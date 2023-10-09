from collections import defaultdict
from functools import cache


class Solution:
    def specialPerm(self, nums: list[int]) -> int:
        n, MOD = len(nums), 10**9 + 7
        nei = defaultdict(list)
        nums.sort()
        ret = 0
        for i in range(n):
            for j in range(i+1, n):
                if nums[j] % nums[i] == 0:
                    nei[j].append(i)
                    nei[i].append(j)
        nei[-1] = range(n)

        dp = [[-1 for _ in range(1 << n)] for _ in range(n)]

        def dfs(prev, mask):
            if mask == (1 << n) - 1:
                dp[prev][mask] = 1
                return 1
            if dp[prev][mask] != -1:
                return dp[prev][mask]
            count = 0
            for i in nei[prev]:
                if not (mask & (1 << i)):  # i is not used in dfs
                    count += dfs(i, mask | (1 << i))
            dp[prev][mask] = count
            return count
        return dfs(-1, 0) % MOD


# inspired by this follow solution:
# class Solution:
#     def specialPerm(self, nums: list[int]) -> int:
#         n, MOD = len(nums), 10**9 + 7

#         @cache
#         def dfs(prev, mask):
#             if mask == (1 << n) - 1:
#                 return 1
#             count = 0
#             for i in range(n):
#                 if not (mask & (1 << i)) and (nums[i] % prev == 0 or prev % nums[i] == 0):
#                     count += dfs(nums[i], mask | (1 << i))
#             return count
#         return dfs(1, 0) % MOD
