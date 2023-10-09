# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

#         1
#     2       3
# 4   5      6    7

# 4, 5, 2, 6, 7, 3, 1
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        st, visit, res = [root], set(), []
        cur = root
        while st:
            cur = st.pop()
            if cur:
                if cur in visit:
                    res.append(cur.val)
                else:
                    st.append(cur)
                    visit.add(cur)
                    st.append(cur.right)
                    st.append(cur.left)
        return res
