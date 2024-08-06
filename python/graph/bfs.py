from collections import deque
from itertools import product
from typing import List

# another problem, two places to check visit


class Solution:
    def maximumSafenessFactor(self, grid: List[List[int]]):
        n = len(grid)
        queue = deque()
        unseen = set(product(range(n), range(n)))

        def nei(x, y):
            return set(((x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1))) & unseen

        # ((x-1, y), (x, y-1), (x+1, y), (x, y+1))) - seen

        queue.append((0, 0, 0))
        unseen.discard((0, 0))
        while queue:
            s, x, y = queue.popleft()
            for nx, ny in nei(x, y):
                unseen.discard((nx, ny))
                queue.append((s + 1, nx, ny))
