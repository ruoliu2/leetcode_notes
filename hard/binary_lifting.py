class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        # n = len(receiver)
        # if k <= 0:
        #     return n - 1
        # dp = [0] * n
        # for i in range(n):
        #     dp[i] = i
        # for _ in range(1, k+1):
        #     newdp = [0] * n
        #     for i in range(n):
        #         newdp[i] = dp[receiver[i]] + i
        #     dp = newdp
        # return max(dp)

        # m, n = k.bit_length(), len(receiver)
        # # pos[i][j] means the end point after move 2^i steps from j
        # pos = [[0] * n for j in range(m)]
        # # profit[i][j] means the profit after move 2^i steps from j, not include j itself
        # profit = [[0] * n for j in range(m)]

        # pos[0] = receiver[:]
        # profit[0] = receiver[:]

        # for i in range(1, m):
        #     for j in range(n):
        #         pos[i][j] = pos[i-1][pos[i-1][j]]
        #         profit[i][j] = profit[i-1][j] + profit[i-1][pos[i-1][j]]

        # def max_profit(idx, curk):
        #     if curk == -1:
        #         return 0
        #     if (k & (1 << curk)) == 0:
        #         return max_profit(idx, curk - 1)
        #     return profit[curk][idx] + max_profit(pos[curk][idx], curk - 1)

        # # since 0 idxed => m steps in total
        # return max([max_profit(i, m - 1) + i for i in range(n)])

        LOG = k.bit_length() + 1
        n = len(receiver)
        P = [receiver[:] for _ in range(LOG)]
        S = [list(range(n)) for _ in range(LOG)]

        for i in range(1, LOG):
            for j in range(n):
                P[i][j] = P[i - 1][P[i - 1][j]]
                S[i][j] = S[i - 1][j] + S[i - 1][P[i - 1][j]]

        res = 0
        for j in range(n):
            score = 0
            for bit in range(LOG):
                if (k + 1) >> bit & 1:
                    score += S[bit][j]
                    j = P[bit][j]
            res = max(res, score)
        return res
