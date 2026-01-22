"""
Evaluate String Expression II (Affirm / LC 224 variant)

Evaluate Lisp-style expressions: ( op arg1 arg2 ... )
Example: "( add 1 2 ( mul 3 4 5 ) 6 )" = 1 + 2 + 60 + 6 = 69
"""
from math import prod


def evaluate(expr: str) -> int:
    tokens = iter(expr.replace("(", " ( ").replace(")", " ) ").split())

    def parse(tok):
        if tok != "(":
            return int(tok)
        op, args = next(tokens), []
        while (tok := next(tokens)) != ")":
            args.append(parse(tok))
        return sum(args) if op == "add" else prod(args)

    return parse(next(tokens))


if __name__ == "__main__":
    print(evaluate("( add 1 2 ( mul 3 4 5 ) 6 )"))  # 69
    # 1 + 2 + (3*4*5) + 6 = 1 + 2 + 60 + 6 = 69

    print(evaluate("( mul ( add 1 2 ) ( mul 3 4 ) ( add 5 6 ) )"))  # 396
    # (1+2) * (3*4) * (5+6) = 3 * 12 * 11 = 396

    print(evaluate("( mul ( mul 2 3 ) ( add 1 ( mul 4 5 ) ) )"))  # 126
    # (2*3) * (1 + (4*5)) = 6 * 21 = 126
