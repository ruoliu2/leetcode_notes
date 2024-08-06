from typing import List


class UnionFind:
    def __init__(self, n):
        self.par = list(range(n))
        self.rank = [1] * n

    def find(self, n1):
        while n1 != self.par[n1]:
            self.par[n1] = self.par[self.par[n1]]
            n1 = self.par[n1]
        return n1

    def union(self, n1, n2):
        p1, p2 = self.find(n1), self.find(n2)
        if p1 == p2:
            return 0
        if self.rank[p2] > self.rank[p1]:
            p1, p2 = p2, p1
        self.par[p2] = p1
        self.rank[p1] += self.rank[p2]
        return 1

    def isConnected(self):
        return max(self.rank) == len(self.rank)


# 1489
class Solution:
    def findCriticalAndPseudoCriticalEdges(
        self, n: int, edges: List[List[int]]
    ) -> List[List[int]]:
        # Time: O(E^2) - UF operations are assumed to be approx O(1)
        for i, e in enumerate(edges):
            e.append(i)  # [v1, v2, weight, original_index]

        edges.sort(key=lambda e: e[2])

        def findWeight(visit, uf, wei):
            for v1, v2, w, i in edges:
                if i != visit and uf.union(v1, v2):
                    wei += w
            return wei

        uf = UnionFind(n)
        mst_wei = findWeight(-1, uf, 0)

        critical, pseudo = [], []
        for n1, n2, e_wei, i in edges:
            # Try without curr edge
            uf = UnionFind(n)
            wei = findWeight(i, uf, 0)
            if not uf.isConnected() or wei > mst_wei:
                critical.append(i)
                continue

            # Try with curr edge
            uf = UnionFind(n)
            uf.union(n1, n2)
            wei = findWeight(-1, uf, e_wei)
            if wei == mst_wei:
                pseudo.append(i)
        return [critical, pseudo]
