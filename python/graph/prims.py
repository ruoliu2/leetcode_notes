# MST
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
