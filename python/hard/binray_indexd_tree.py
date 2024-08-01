class BIT:
    def __init__(self, size):
        self.tree = [0] * (size + 1)
        self.size = size

    def update(self, i, value):
        # update element at index i by value
        i += 1
        while i <= self.size:
            self.tree[i] += value
            i += self.low_bit(i)

    def getSum(self, i):
        # get sum of elements from 0 to i inclusive
        preSum, i = 0, i + 1
        while i > 0:
            preSum += self.tree[i]
            i -= self.low_bit(i)
        return preSum

    @staticmethod
    def low_bit(x):
        return x & -x


class Solution:
    def numTeams(self, rating: List[int]) -> int:
        n = len(rating)
        if n < 3:
            return 0

        # Coordinate compression to handle large values in BIT
        rating_sorted = sorted(rating)
        rtoi = {val: i for i, val in enumerate(rating_sorted)}

        cnt_l = BIT(n)
        cnt_r = BIT(n)

        # Populate right BIT with all elements
        for r in rating:
            cnt_r.update(rtoi[r], 1)

        res = 0
        for i in range(n):
            cnt_r.update(rtoi[rating[i]], -1)
            ll = cnt_l.getSum(rtoi[rating[i]])
            rg = cnt_r.getSum(n - 1) - cnt_r.getSum(rtoi[rating[i]])

            res += ll * rg + (i - ll) * (n - i - rg - 1)
            cnt_l.update(rtoi[rating[i]], 1)

        return res


class NumArray:

    def __init__(self, nums: List[int]):
        self.nums = nums
        self.tree = BIT(nums)

    def update(self, i: int, val: int) -> None:
        self.tree.update(i, val - self.nums[i])
        self.nums[i] = val

    def sumRange(self, l: int, r: int) -> int:
        # BIT is 1 based tree, right will be added by 1, done in BIT alr
        # For range sum from l to r, we need to get sum from 0 to r and subtract sum from 0 to l - 1
        return self.tree.getSum(r) - self.tree.getSum(l - 1)
