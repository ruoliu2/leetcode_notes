class UF:
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


class Solution:
    # 947
    def removeStones(self, stones: list[list[int]]) -> int:
        uf = {}

        def find(node):
            if node != uf.setdefault(node, node):
                uf[node] = find(uf[node])
            return uf[node]

        for r, c in stones:
            uf[find(r)] = find(~c)
        return len(stones) - len({find(node) for node in uf})
