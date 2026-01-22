"""
Decision Tree (Affirm)

Build a decision tree for loan approval based on signals (FICO score, income, etc.)

API:
  add_split(leaf, signal_name, constant) -> [left_leaf, right_leaf]
    - Add split condition to leaf node, return two new leaves
    - Pass None for first call to create root

  set_leaf_value(leaf, value)
    - Set return value (Y/N) for a leaf node

  evaluate(signals) -> value
    - Traverse tree with signal_name -> signal_value mapping
    - If signal_value < constant: go left, else: go right

Example Tree:
           X1 < 3
        ------------
       |            |
    X2 < 1       X1 < 6
 -----------    ---------
|           |  |         |
N           Y  N      X3 < 2
                    ----------
                   |          |
                   Y          N

evaluate({X1: 2, X2: 11, X3: 1}) -> Y  (X1<3 -> left, X2<1 false -> right)
"""


class Node:
    def __init__(self):
        self.signal = None      # signal name for split
        self.constant = None    # threshold for split
        self.left = None        # < constant
        self.right = None       # >= constant
        self.value = None       # leaf value (Y/N)

    def is_leaf(self):
        return self.left is None and self.right is None


class DecisionTree:
    def __init__(self):
        self.root = None

    def add_split(self, leaf: Node, signal_name: str, constant: float) -> list[Node]:
        """Add split condition to leaf, return [left_leaf, right_leaf]."""
        if leaf is None:
            # First call - create root
            self.root = Node()
            leaf = self.root

        leaf.signal = signal_name
        leaf.constant = constant
        leaf.left = Node()
        leaf.right = Node()
        leaf.value = None  # no longer a leaf with value

        return [leaf.left, leaf.right]

    def set_leaf_value(self, leaf: Node, value):
        """Set return value for a leaf node."""
        leaf.value = value

    def evaluate(self, signals: dict) -> any:
        """Traverse tree and return leaf value."""
        cur = self.root
        while not cur.is_leaf():
            if signals[cur.signal] < cur.constant:
                cur = cur.left
            else:
                cur = cur.right
        return cur.value


if __name__ == "__main__":
    tree = DecisionTree()

    # Build:    X1 < 3
    #        ------------
    #       |            |
    #    X2 < 1          N
    # -----------
    #|           |
    #N           Y

    left1, right1 = tree.add_split(None, "X1", 3)
    tree.set_leaf_value(right1, "N")

    left2, right2 = tree.add_split(left1, "X2", 1)
    tree.set_leaf_value(left2, "N")
    tree.set_leaf_value(right2, "Y")

    print(tree.evaluate({"X1": 2, "X2": 0}))   # N (X1<3 left, X2<1 left)
    print(tree.evaluate({"X1": 2, "X2": 11}))  # Y (X1<3 left, X2<1 false right)
    print(tree.evaluate({"X1": 5, "X2": 0}))   # N (X1<3 false right)

    # Build full example tree from docstring
    tree2 = DecisionTree()
    l1, r1 = tree2.add_split(None, "X1", 3)

    l2, r2 = tree2.add_split(l1, "X2", 1)
    tree2.set_leaf_value(l2, "N")
    tree2.set_leaf_value(r2, "Y")

    l3, r3 = tree2.add_split(r1, "X1", 6)
    tree2.set_leaf_value(l3, "N")

    l4, r4 = tree2.add_split(r3, "X3", 2)
    tree2.set_leaf_value(l4, "Y")
    tree2.set_leaf_value(r4, "N")

    print(tree2.evaluate({"X1": 2, "X2": 11, "X3": 1}))  # Y
    print(tree2.evaluate({"X1": 4, "X2": 0, "X3": 0}))   # N (X1>=3 right, X1<6 left)
    print(tree2.evaluate({"X1": 7, "X2": 0, "X3": 1}))   # Y (X1>=3, X1>=6, X3<2)
    print(tree2.evaluate({"X1": 7, "X2": 0, "X3": 5}))   # N (X1>=3, X1>=6, X3>=2)
