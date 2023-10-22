# 743   single source shortest path
import collections
import heapq
from typing import List
from itertools import product
from heapq import heappop, heappush
from collections import deque


class Solution1:
    def maximumSafenessFactor(self, grid: List[List[int]]) -> int:
        n, m = len(grid), len(grid[0])
        queue, safeness = deque(), [[-1] * n for _ in range(n)]
        unseen = set(product(range(n), range(n)))

        def nei(x, y): return set(
            ((x-1, y), (x, y-1), (x+1, y), (x, y+1))) & unseen

        hp = [(-safeness[-1][-1], n-1, m-1)]
        unseen.discard((n-1, m-1))
        while hp:
            s, x, y = heappop(hp)
            if (x, y) == (0, 0):
                print(min(-s, safeness[0][0]))
            for nx, ny in nei(x, y):
                safe = max(s, -safeness[nx][ny])
                heappush(hp, (safe, nx, ny))
                unseen.discard((nx, ny))
        return -1


class Solution2:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        graph = collections.defaultdict(list)
        for u, v, w in times:
            graph[u].append([v, w])
        hp = [(0, k)]
        dist = {}
        while hp:
            w, v = heapq.heappop(hp)
            if v not in dist:
                dist[v] = w
                for nei, neiDist in graph[v]:
                    heapq.heappush(hp, (w + neiDist, nei))
        # dist is the dist to every node from k
