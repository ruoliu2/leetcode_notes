class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        n = len(nums)
        nums.append(float('inf'))

        dp = [[0] * (n+1) for i in range(n)]
        # dp[i][j] = length of LIS ending at nums[i] with nums[i] < nums[j]
        for i in range(n):
            for j in range(i+1, n+1):
                dp[i][j] = dp[i-1][j]
                if nums[i] < nums[j]:
                    dp[i][j] = max(dp[i][j], dp[i-1][i] + 1)

        return dp[-1][-1]

    def LIS(self, nums):
        sub = []
        for num in nums:
            i = bisect_left(sub, num)
            if i == len(sub):
                sub.append(num)
            else:
                sub[i] = num
        return len(sub)
