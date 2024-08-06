"""
all pairs shortest path
If i can reach k and k can reach j and dist(k, k, k-1) < 0 then G
has a negative length cycle containing k and dist(i, j, k) = -INF.

Recursion below is valid only if dist(k, k, k- 1) >= 0.
"""

INF = float("inf")


def floyd_warshall(graph):
    n = len(graph)
    dist = [float("inf") * n for _ in range(n)]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                # If vertex k is on the shortest path from
                # i to j, then update the value of dist[i][j]
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    print_solution(dist)


def print_solution(dist):
    n = len(dist)
    for i in range(n):
        for j in range(n):
            if dist[i][j] == INF:
                print(f"{INF:>7}", end=" ")
            else:
                print(f"{dist[i][j]:>7d}", end=" ")
            if j == n - 1:
                print()
