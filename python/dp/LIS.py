from bisect import bisect_left


class Solution:
    def lengthOfLIS1D(self, nums: list[int]) -> int:
        # f[i] = 1 + max(f[j] for j in range(i + 1, n) if nums[j] > nums[i])
        dp = [1] * len(nums)
        for i in range(len(nums) - 1, -1, -1):
            for j in range(i + 1, len(nums)):
                if nums[j] > nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)

    def lengthOfLIS2D(self, nums: list[int]) -> int:
        # cnt[i, j] LIS s.t LIS in nums[0...i] (not includes i) less than nums[j]
        # cnt[i, j] = cnt[i - 1, j]
        # max(cnt[i, j], cnt[i - 1, i] + 1) if nums[i] < nums[j]

        # base case cnt[0, k] = 0
        n = len(nums)
        cnt = [[0] * n for i in range(n - 1)]
        res = 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                cnt[i][j] = cnt[i - 1][j]
                if nums[i] < nums[j]:
                    cnt[i][j] = max(cnt[i][j], cnt[i - 1][i] + 1)
                res = max(res, cnt[i][j])
        return res + 1

    def lengthOfLISStack(self, nums):
        sub = []
        for num in nums:
            i = bisect_left(sub, num)
            if i == len(sub):
                sub.append(num)
            else:
                sub[i] = num
        return len(sub)
