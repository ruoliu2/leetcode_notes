# max stack


@total_ordering
class Node:
    def __init__(
        self, val: int = -1, pos: int = -1
    ):  # return -1 to peek/pop when st is empty
        self.val = val
        self.pos = pos
        self.prev = None
        self.next = None
        self.alive = True

    def __eq__(self, other):
        return self.val == other.val and self.pos == other.pos

    def __lt__(self, other):
        if self.val > other.val:
            return True
        elif self.val == other.val:
            return self.pos > other.pos
        return False


class MaxStack:

    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.hp = []
        self.pos = 0

    def _insert_after(self, node, new_node):
        new_node.prev = node
        new_node.next = node.next
        node.next.prev = new_node
        node.next = new_node

    def _delete(self, node):
        if node.prev is None or node.next is None:  # don't delete head or tail
            return
        node.alive = False
        node.prev.next = node.next
        node.next.prev = node.prev

    def push(self, v: int) -> None:
        new_node = Node(v, self.pos)
        self._insert_after(self.tail.prev, new_node)
        heappush(self.hp, new_node)
        self.pos += 1

    def pop(self) -> int:
        curr = self.tail.prev
        while not curr.alive:
            curr = curr.prev
        self._delete(curr)
        return curr.val

    def top(self) -> int:
        curr = self.tail.prev
        while not curr.alive:
            curr = curr.prev
        return curr.val

    def peekMax(self) -> int:
        while not self.hp[0].alive:
            heappop(self.hp)
        return self.hp[0].val

    def popMax(self) -> int:
        while not self.hp[0].alive:
            heappop(self.hp)
        top = heappop(self.hp)
        self._delete(top)
        return top.val
