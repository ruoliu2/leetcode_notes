class Solution:
    # 435
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x: x[1])
        res, prev = 0, -inf
        for s, e in intervals:
            if s < prev:
                res += 1
            else:
                prev = e
        return res
