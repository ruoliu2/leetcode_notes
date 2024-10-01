# 1014
class Solution:
    def maxScoreSightseeingPair(self, values: list[int]) -> int:
        res = cur = 0
        for i in range(1, len(values)):
            cur = max(cur, values[i - 1] + i - 1)
            res = max(res, cur + values[i] - i)
        return res
