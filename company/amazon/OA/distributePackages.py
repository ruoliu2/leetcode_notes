class Solution:
    def distributePackages(self, trucks: list[int], to_distribute: int) -> list[int]:
        return max(max(trucks), ceil(sum(trucks) + to_distribute) / len(trucks))
