# 2863
class Solution:
    def maxSubarrayLength(self, nums: list[int]) -> int:
        st = []
        n = len(nums)
        for i in range(n-1, -1, -1):
            if not st or nums[st[-1]] > nums[i]:
                st.append(i)
        res = 0
        for i in range(n):
            while st and nums[i] > nums[st[-1]]:
                res = max(res, st.pop() - i + 1)
        return res
