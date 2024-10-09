class Solution:
    # 452
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        points.sort(reverse=True)
        pre = points[0][0]
        res = 1
        for s, e in points[1:]:
            if e < pre:
                res += 1
                pre = s
        return res
