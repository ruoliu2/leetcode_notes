# 743   single source shortest path
import collections
import heapq
from typing import List


class Solution:
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
