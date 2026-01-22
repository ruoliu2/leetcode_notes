"""
Persistent Stack (Affirm)

Immutable stack where push/pop return NEW instances, originals unchanged.
All operations O(1). All versions remain accessible.

Example:
  stack1 = PStack()           # []
  stack2 = stack1.push(10)    # [10]
  stack3 = stack2.push(20)    # [20, 10]
  stack4 = stack3.push(30)    # [30, 20, 10]
  stack5 = stack4.pop()       # [20, 10]
  # stack4 still has [30, 20, 10]

Core idea: Linked list nodes, shared tail. Push creates new head pointing to old.
           Pop returns reference to tail. O(1) because no copying.

  stack4: 30 -> 20 -> 10 -> None
  stack5:       20 -> 10 -> None  (same nodes, just different head)
"""


class PStack:
    def __init__(self, head=None, size=0):
        self._head = head  # (val, prev_node) or None
        self._size = size

    def size(self) -> int:
        return self._size

    def peek(self) -> int:
        return self._head[0]

    def push(self, val: int) -> "PStack":
        # New node points to current head
        return PStack((val, self._head), self._size + 1)

    def pop(self) -> "PStack":
        # Return stack starting from prev node
        return PStack(self._head[1], self._size - 1)

    def to_list(self) -> list[int]:
        """Helper for visualization."""
        result, node = [], self._head
        while node:
            result.append(node[0])
            node = node[1]
        return result


if __name__ == "__main__":
    stack1 = PStack()
    stack2 = stack1.push(10)
    stack3 = stack2.push(20)
    stack4 = stack3.push(30)

    print(f"stack1: {stack1.to_list()}")  # []
    print(f"stack2: {stack2.to_list()}")  # [10]
    print(f"stack3: {stack3.to_list()}")  # [20, 10]
    print(f"stack4: {stack4.to_list()}")  # [30, 20, 10]
    print(f"size: {stack4.size()}")       # 3
    print(f"peek: {stack4.peek()}")       # 30

    stack5 = stack4.pop()
    print(f"stack5: {stack5.to_list()}")  # [20, 10]
    print(f"stack4 unchanged: {stack4.to_list()}")  # [30, 20, 10]
