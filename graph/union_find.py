class UF:
    def __init__(self, n):
        self.par = list(range(n))
        self.rank = [1] * n

    def find(self, n1):
        p1 = n1
        while p1 != self.par[p1]:
            self.par[p1] = self.par[self.par[p1]]
            p1 = self.par[p1]
        return p1

    def union(self, n1, n2):
        p1, p2 = self.find(n1), self.find(n2)
        if p1 == p2:
            return 0
        if self.rank[p2] > self.rank[p1]:
            p1, p2 = p2, p1
        self.par[p2] = p1
        self.rank[p1] += self.rank[p2]
        return 1
