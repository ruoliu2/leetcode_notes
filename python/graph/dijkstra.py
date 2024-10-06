import collections
import heapq
import itertools


class Solution:
    # 2812
    def maximumSafenessFactor(self, grid: list[list[int]]) -> int:
        n, m = len(grid), len(grid[0])
        safeness = [[-1] * n for _ in range(n)]
        unseen = set(itertools.product(range(n), range(n)))

        def nei(x, y):
            return set(((x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1))) & unseen

        # set - visit
        hp = [(-safeness[-1][-1], n - 1, m - 1)]
        unseen.discard((n - 1, m - 1))
        while hp:
            s, x, y = heapq.heappop(hp)
            if (x, y) == (0, 0):
                print(min(-s, safeness[0][0]))
            for nx, ny in nei(x, y):
                safe = max(s, -safeness[nx][ny])
                heapq.heappush(hp, (safe, nx, ny))
                unseen.discard((nx, ny))
        return -1

    # 743   single source shortest path
    def networkDelayTime(self, times: list[list[int]], n: int, k: int) -> int:
        graph = collections.defaultdict(list)
        for u, v, w in times:
            graph[u].append([v, w])
        hp = [(0, k)]
        dist = {}
        while hp:
            w, v = heapq.heappop(hp)
            if v in dist:
                continue
            dist[v] = w
            for nei, neiDist in graph[v]:
                heapq.heappush(hp, (w + neiDist, nei))
        # dist is the dist to every node from k
