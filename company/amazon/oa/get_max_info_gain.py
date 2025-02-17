class Solution:
    def getMaxInformationGain(
        self, dataSet: list[str], max_common_features: int
    ) -> int:
        n = len(dataSet)
        dataSet.sort(key=len)
        l, r = 0, n - 1
        res = 0

        def available(l, r):
            c1, c2 = [0] * 26, [0] * 26
            for ch in dataSet[l]:
                c1[ord(ch) - ord("a")] += 1
            for ch in dataSet[r]:
                c2[ord(ch) - ord("a")] += 1
            res = 0
            for i in range(26):
                res += min(c1[i], c2[i])
            return res <= max_common_features

        def solve(l, r):
            if l >= r:
                return 0
            if available(l, r):
                return len(dataSet[r]) - len(dataSet[l])
            return max(solve(l + 1, r), solve(l, r - 1))

        return solve(l, r)
