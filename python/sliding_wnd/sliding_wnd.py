from typing import List


# 1004
class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        l = 0
        res = 0
        for r, val in enumerate(nums):
            k -= 1 - val
            while k < 0:
                k += 1 - nums[l]
                l += 1
            res = max(res, r - l + 1)
        return res
