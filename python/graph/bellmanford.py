"""
single source shortest path
for each u in V:
    d[u] = inf
d[s] = 0
for k in range(n):
    for each edge (u,v) in G:
        d[v] = min(d[v], d[u] + l[u,v])
for each v in V:
    dist[(s,v)] = d[v]
    
time:  O(mn)
space: O(n)
    
"""


class Solution:
    def findCheapestPrice(
        self, n: int, flights: list[list[int]], src: int, dst: int, k: int
    ) -> int:
        prices = [float("inf")] * n
        prices[src] = 0
        for _ in range(k + 1):
            tmp = prices[:]
            for s, d, p in flights:
                prices[d] = min(prices[s] + p, tmp[d])
            prices = tmp
        return prices[dst] if prices[dst] != float("inf") else -1

    # 1514
    def maxProbability(
        self,
        n: int,
        edges: list[list[int]],
        succProb: list[float],
        start: int,
        end: int,
    ) -> float:
        dist = [0] * n
        dist[start] = 1

        for _ in range(n - 1):
            update = 0
            for i, (u, v) in enumerate(edges):
                if dist[u] * succProb[i] > dist[v]:
                    dist[v] = dist[u] * succProb[i]
                    update = 1
                if dist[v] * succProb[i] > dist[u]:
                    dist[u] = dist[v] * succProb[i]
                    update = 1
            if not update:
                break

        return dist[end]
