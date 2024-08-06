class Solution:
    def getMaxFunctionValue(self, receiver: list[int], k: int) -> int:
        m, n = k.bit_length(), len(receiver)
        # pos[i][j] means the end point after move 2^i steps from j
        pos = [[0] * n for j in range(m)]
        # profit[i][j] means the profit after move 2^i steps from j, not include j itself
        profit = [[0] * n for j in range(m)]

        pos[0] = receiver[:]
        profit[0] = receiver[:]

        for i in range(1, m):
            for j in range(n):
                pos[i][j] = pos[i - 1][pos[i - 1][j]]
                profit[i][j] = profit[i - 1][j] + profit[i - 1][pos[i - 1][j]]

        def max_profit(idx, curk):
            if curk == -1:
                return 0
            if (k & (1 << curk)) == 0:
                return max_profit(idx, curk - 1)
            return profit[curk][idx] + max_profit(pos[curk][idx], curk - 1)

        # since 0 idxed => m steps in total
        return max([max_profit(i, m - 1) + i for i in range(n)])
