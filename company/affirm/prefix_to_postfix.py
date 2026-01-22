"""
Prefix to Postfix (Affirm)

Convert prefix expression to postfix.
  Prefix:  operator before operands  "*+AB-CD" = (A+B)*(C-D)
  Postfix: operator after operands   "AB+CD-*"

Approach: Scan right to left, use stack.
  - Operand: push to stack
  - Operator: pop two, combine as "op1 + op2 + operator", push back

Time: O(n), Space: O(n)
"""


def prefix_to_postfix(prefix: str) -> str:
    stack = []
    operators = {"+", "-", "*", "/"}

    # Scan right to left
    for ch in reversed(prefix):
        if ch in operators:
            # Pop two operands, combine: op1 + op2 + operator
            op1 = stack.pop()
            op2 = stack.pop()
            stack.append(op1 + op2 + ch)
        else:
            # Operand (digit or letter)
            stack.append(ch)

    return stack[0]


if __name__ == "__main__":
    print(prefix_to_postfix("+12"))       # "12+"
    print(prefix_to_postfix("-*345"))     # "34*5-"
    print(prefix_to_postfix("*+AB-CD"))   # "AB+CD-*"
