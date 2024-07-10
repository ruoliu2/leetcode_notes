class BIT:
    def __init__(self, nums):
        self.tree = [0] + nums
        self.n = len(self.tree)
        for i in range(1, self.n):
            p = i + self.low_bit(i)
            if p < self.n:
                self.tree[p] += self.tree[i]

    def update(self, i, value):
        while i < self.n:
            self.tree[i] += value
            i += self.low_bit(i)

    def getSum(self, i):
        preSum = 0
        while i > 0:
            preSum += self.tree[i]
            i -= self.low_bit(i)
        return preSum

    @staticmethod
    def low_bit(bit):
        return bit & -bit


class NumArray:

    def __init__(self, nums: list[int]):
        self.nums = nums
        self.tree = BIT(nums)

    def update(self, i: int, val: int) -> None:
        self.tree.update(i + 1, val - self.nums[i])
        self.nums[i] = val

    def sumRange(self, l: int, r: int) -> int:
        return self.tree.getSum(r + 1) - self.tree.getSum(l)
