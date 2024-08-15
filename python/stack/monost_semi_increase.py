# 2863
class Solution:
    def maxSubarrayLength(self, nums: list[int]) -> int:
        st = []
        n = len(nums)
        for i in range(n - 1, -1, -1):
            if not st or nums[st[-1]] > nums[i]:
                st.append(i)
        res = 0
        for i in range(n):
            while st and nums[i] > nums[st[-1]]:
                res = max(res, st.pop() - i + 1)
        return res

    def maximumScore(self, nums: list[int], k: int) -> int:
        n = len(nums)
        l, r = [-1] * n, [n] * n
        st = []
        for i in range(n - 1, -1, -1):
            while st and nums[st[-1]] > nums[i]:
                l[st.pop()] = i
            st.append(i)
        st = []
        for i in range(n):
            while st and nums[st[-1]] > nums[i]:
                r[st.pop()] = i
            st.append(i)
        res = 0
        for i in range(n):
            if l[i] < k < r[i]:
                res = max(res, nums[i] * (r[i] - l[i] - 1))
        return res
