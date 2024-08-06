# 1584. Min Cost to Connect All Points
# MST
import collections
import heapq


class Solution:
    def minCostConnectPoints(self, points: list[list[int]]) -> int:
        n = len(points)
        graph = collections.defaultdict(list)
        for i in range(n):
            for j in range(i + 1, n):
                mdist = abs(points[i][0] - points[j][0]) + abs(
                    points[i][1] - points[j][1]
                )
                graph[i].append([j, mdist])
                graph[j].append([i, mdist])
        # above making graph

        hp = [[0, 0]]
        res = 0
        visit = set()
        while len(visit) < n:
            cost, idx = heapq.heappop(hp)
            if idx in visit:
                continue
            res += cost
            visit.add(idx)
            for nei, nei_cost in graph[idx]:
                if nei not in visit:
                    heapq.heappush(hp, [nei_cost, nei])
        return res
