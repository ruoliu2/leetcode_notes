# MST
import collections
import heapq
from typing import List


# 1489
class Solution:
    def findCriticalAndPseudoCriticalEdges(
        self, n: int, edges: List[List[int]]
    ) -> List[List[int]]:
        edges = [(a, b, c, i) for i, (a, b, c) in enumerate(edges)]
        edges.sort(key=lambda x: x[2])
        maxCost = 1000 * 100

        def getMSTCost(E, V, C):
            """
            E: edge exclusive set
            V: nodes in MST
            C: current Cost
            """
            nonlocal edges, n, maxCost
            if len(V) == n:
                return C
            else:
                for a, b, c, i in edges:
                    if i not in E and (a in V and b not in V or a not in V and b in V):
                        return getMSTCost(E | set([i]), V | set([a, b]), C + c)
            return maxCost

        C = getMSTCost(set(), set([0]), 0)

        critical, pseudo_critical = [], []
        for a, b, c, i in edges:
            if getMSTCost(set([i]), set([0]), 0) > C:
                critical += [i]
            elif getMSTCost(set([i]), set([a, b]), c) == C:
                pseudo_critical += [i]

        return [critical, pseudo_critical]

    #
    #
    # 1584. Min Cost to Connect All Points
    #
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
