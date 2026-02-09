class AVLTree:
    class Node:
        __slots__ = ("val", "left", "right", "h")

        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None
            self.h = 1  # height

    def __init__(self):
        self.root = None

    # ----- helpers -----
    def _height(self, node):
        return node.h if node else 0

    def _update_height(self, node):
        node.h = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_right(self, y):
        x = y.left
        t2 = x.right
        x.right = y
        y.left = t2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        t2 = y.left
        y.left = x
        x.right = t2
        self._update_height(x)
        self._update_height(y)
        return y

    # ----- core ops -----
    def _insert(self, node, key):
        # 1) normal BST insert
        if not node:
            return self.Node(key)
        if key < node.val:
            node.left = self._insert(node.left, key)
        elif key > node.val:
            node.right = self._insert(node.right, key)
        else:
            return node  # ignore duplicates; change if you want counts

        # 2) update height
        self._update_height(node)

        # 3) rebalance
        balance = self._height(node.left) - self._height(node.right)

        # LL
        if balance > 1 and key < node.left.val:
            return self._rotate_right(node)
        # RR
        if balance < -1 and key > node.right.val:
            return self._rotate_left(node)
        # LR
        if balance > 1 and key > node.left.val:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        # RL
        if balance < -1 and key < node.right.val:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def search(self, key):
        node = self.root
        while node:
            if key < node.val:
                node = node.left
            elif key > node.val:
                node = node.right
            else:
                return True
        return False

    # optional: inorder traversal for debugging
    def inorder(self):
        res = []

        def dfs(node):
            if not node:
                return
            dfs(node.left)
            res.append(node.val)
            dfs(node.right)

        dfs(self.root)
        return res


avl = AVLTree()
for x in [10, 20, 30, 40, 50, 25]:
    avl.insert(x)

print(avl.search(25))  # True
print(avl.search(99))  # False
print(avl.inorder())  # sorted keys
