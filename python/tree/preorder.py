# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res = []

        node = root
        st = []
        while st or node:
            if node:
                res.append(node.val)
                st.append(node.right)
                node = node.left
            else:
                node = st.pop()
        return res
