class Solution:
    def minSumDistancesToWarehouses(self, dist_centers: list[int]) -> int:
        dist_centers.sort()
        n = len(dist_centers)
        pre_m = [0] * n
        suf_m = [0] * n
        for i in range(n):
            pre_m[i] = dist_centers[i // 2]
        for i in range(n - 1, -1, -1):
            suf_m[i] = dist_centers[(i + n) // 2]
        dist_p = [0] * n
        dist_s = [0] * n
        for i in range(n):
            dist_p[i] = abs(dist_centers[i] - pre_m[i])
            dist_s[i] = abs(dist_centers[i] - suf_m[i])
        sum_p = [0] * n
        sum_s = [0] * n
        sum_p[0] = dist_p[0]
        sum_s[n - 1] = dist_s[n - 1]
        # why does this work?
        # the first half and second half increase amount and decrease amount due to move of the median are the same
        # then the only increasing amount is the distance to its median
        for i in range(1, n):
            sum_p[i] = sum_p[i - 1] + dist_p[i]
        for i in range(n - 2, -1, -1):
            sum_s[i] = sum_s[i + 1] + dist_s[i]
        res = float("inf")
        for i in range(n - 1):
            res = min(res, sum_p[i] + sum_s[i + 1])
        return res
