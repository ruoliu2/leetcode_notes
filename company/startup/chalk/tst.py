# useful Python metaprogramming tools

# step 1:
########

# cls.__annotations__
# cls.__name__
# setattr(obj, key, value)

import dataclasses
from typing import Callable, Any, TypeVar, ParamSpec, Generic

"""
STEP 1: Parse features
"""


@dataclasses.dataclass(unsafe_hash=True)
class Feature:
    name: str  # eg. User.name
    typ: type  # eg. str

_class_by_name: {str: type} = {}
_pending_feature_classes: list[type] = []

def build_features():
    """
    Second pass:
    - run after all @features classes are defined
    - resolves forward refs like "User"
    - sets cls.features as a plain list[Feature]
    """
    for cls in _pending_feature_classes:
        flist = []
        for attr_name, ann in cls.__annotations__.items():
            if isinstance(ann, str):
                ann = _class_by_name[ann]  # resolve "User" -> User
            feat = Feature(name=f"{cls.__name__}.{attr_name}", typ=ann)
            flist.append(feat)
            setattr(cls, attr_name, feat)
        cls.features = flist


def features(cls):
    """Implement me!
    User.features == [
        Feature(name="User.name", typ=str),
        Feature(name="User.card_id", typ=int),
        ...
    ]
    """
    _class_by_name[cls.__name__] = cls
    _pending_feature_classes.append(cls)
    return cls


@features
class Card:
    id: int
    number: str
    owner: "User"


@features
class User:
    id: int
    email: str
    name: str
    card_id: int
    is_fraud: bool

build_features()

def test_scalars():
    assert User.features == [
        Feature(name="User.id", typ=int),
        Feature(name="User.email", typ=str),
        Feature(name="User.name", typ=str),
        Feature(name="User.card_id", typ=int),
        Feature(name="User.is_fraud", typ=bool),
    ], User.features


def test_forward_reference():
    assert Card.features == [
        Feature(name="Card.id", typ=int),
        Feature(name="Card.number", typ=str),
        Feature(name="Card.owner", typ=User),
    ], Card.features

test_scalars()
test_forward_reference()


def test_properties():
    assert User.id == Feature(name="User.id", typ=int)


test_properties()

"""
STEP 2: Parse resolvers
"""

# step 2:
#########
# import inspect

# inspect.signature(fn)

import inspect

P = ParamSpec("P")
T = TypeVar("T")

@dataclasses.dataclass
class Resolver(Generic[P, T]):
    inputs: list[Feature]
    output: Feature
    fn: Callable[P, T]
    
_res: list[Resolver] = []

def resolver(fn: Callable[P, T]) -> Resolver[P, T]:
    """Implement me!"""
    sig = inspect.signature(fn)
    inputs: list[Feature] = []
    for param in sig.parameters.values():
        inputs.append(param.annotation)
    fn.inputs = inputs
    fn.output = sig.return_annotation
    _res.append(Resolver(inputs=fn.inputs, output=fn.output, fn=fn))
    return fn


@resolver
def get_user_name(id: User.id) -> User.name:
    if id == 1:
        return "elliot"
    return "joe"


@resolver
def get_user_email(id: User.id) -> User.email:
    if id == 1:
        return "elliot@chalk.ai"
    return "fraudster@chalk.ai"


@resolver
def get_user_fraud_score(name: User.name, email: User.email) -> User.is_fraud:
    return name.lower() not in email.lower()


def test_resolvers():
    assert get_user_name.output == User.name, get_user_name.output
    assert get_user_name.inputs == [User.id], get_user_name.inputs

    assert get_user_email.output == User.email, get_user_email.output
    assert get_user_email.inputs == [User.id], get_user_email.inputs

    assert get_user_fraud_score.output == User.is_fraud
    assert get_user_fraud_score.inputs == [User.name, User.email]


test_resolvers()

"""
STEP 3: Define a function that takes a list of inputs and desired
outputs, and computes the outputs
"""

def check_resolver(
    inputs: dict[Feature | Any, Any],
    resolver: Resolver,
) -> bool:
    """Return True when all resolver inputs are currently available."""
    available = {feat for feat in inputs if isinstance(feat, Feature)}
    return all(required in available for required in resolver.inputs)

def execute(
    inputs: dict[Feature | Any, Any], outputs: list[Feature | Any]
) -> dict[Feature, Any]:
    """Implement me!
    execute(inputs={User.id: 1}, outputs=[User.is_fraud]) == {User.is_fraud: False}
    """
    known: dict[Feature | Any, Any] = dict(inputs)
    desired = set(outputs)

    while True:
        if desired.issubset({feat for feat in known if isinstance(feat, Feature)}):
            return {feat: known[feat] for feat in outputs}

        progress = False
        for reso in _res:
            if reso.output in known:
                continue
            if check_resolver(known, reso):
                args = [known[inp] for inp in reso.inputs]
                known[reso.output] = reso.fn(*args)
                progress = True

        if not progress:
            return {}


def test_execute():
    assert execute(
        inputs={User.id: 1},
        outputs=[User.is_fraud],
    ) == {User.is_fraud: False}

    assert execute(
        inputs={User.id: 2},
        outputs=[User.is_fraud],
    ) == {User.is_fraud: True}


test_execute()
