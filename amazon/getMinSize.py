class Solution:
    def getMinSize(self, gameSize: list[int], k: int) -> int:
        gameSize.sort(reverse=True)

        def check(size: int) -> bool:
            l, r = 0, len(gameSize) - 1
            cnt = 0
            while l <= r:
                if gameSize[l] + gameSize[r] <= size:
                    l += 1
                    r -= 1
                else:
                    r -= 1
                cnt += 1
            return cnt <= k

        l, r = max(gameSize), 2 * max(gameSize)
        while l < r:
            mid = (l + r) // 2
            if check(mid):
                r = mid
            else:
                l = mid + 1
        return l
