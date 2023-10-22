# another problem, two places to check visit
from typing import List
import collections
from itertools import product
from collections import deque


class Solution:
    def maximumSafenessFactor(self, grid: List[List[int]]) -> int:
        n = len(grid)
        queue, safeness = deque(), [[-1] * n for _ in range(n)]
        unseen = set(product(range(n), range(n)))
        def nei(x, y): return set(
            ((x-1, y), (x, y-1), (x+1, y), (x, y+1))) & unseen

        queue.append((0, 0, 0))
        unseen.discard((0, 0))
        while queue:
            s, x, y = queue.popleft()
            for nx, ny in nei(x, y):
                unseen.discard((nx, ny))
                queue.append((s+1, nx, ny))


class Solution1:  # prefered
    def shortestPath(self, grid: List[List[int]], k: int) -> int:
        m, n = len(grid), len(grid[0])
        dir = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        visit = set([(0, 0, k)])
        if k >= m + n - 2:
            return m + n - 2
        q = collections.deque([])
        q.append((0, 0, 0, k))
        while q:
            steps, x0, y0, rk = q.popleft()
            if rk < 0:
                continue
            if (x0, y0) == (m-1, n-1):
                return steps
            for xd, yd in dir:
                x1, y1 = x0 + xd, y0 + yd
                if (0 <= x1 < m and 0 <= y1 < n
                        and (x1, y1, rk - grid[x1][y1]) not in visit):
                    visit.add((x1, y1, rk - grid[x1][y1]))
                    q.append((steps+1, x1, y1, rk - grid[x1][y1]))
        return -1


# class Solution2:
#     def shortestPath(self, grid: List[List[int]], k: int) -> int:
#         m, n = len(grid), len(grid[0])
#         dir = [(0, 1), (1, 0), (-1, 0), (0, -1)]
#         visit = set([])
#         if k >= m + n - 2:
#             return m + n - 2

#         q = collections.deque([])
#         q.append((0, 0, 0, k))
#         while q:
#             steps, x0, y0, rk = q.popleft()
#             if (x0, y0, rk) in visit or rk < 0:
#                 continue
#             if (x0, y0) == (m-1, n-1):
#                 return steps
#             visit.add((x0, y0, rk))
#             for xd, yd in dir:
#                 x1, y1 = x0 + xd, y0 + yd
#                 if (0 <= x1 < m and 0 <= y1 < n):
#                     q.append((steps+1, x1, y1, rk - grid[x1][y1]))
#         return -1


# # original solution


# def numIslands(grid: list[list[str]]) -> int:
#     if not grid:
#         return 0

#     visit = set()
#     ret = 0
#     row, col = len(grid), len(grid[0])
#     dir = [(1, 0), (-1, 0), (0, 1), (0, -1)]

#     def bfs(r, c):
#         q = []
#         visit.add((r, c))
#         q.append((r, c))
#         while q:
#             (row, col) = q.pop(0)
#             for (dr, dc) in dir:
#                 r, c = row + dr, col + dc
#                 if (
#                     (r, c) not in visit
#                     and r in range(len(grid))
#                     and c in range(len(grid[0]))
#                     and grid[r][c] == "1"
#                 ):
#                     bfs(r, c)

#     for i in range(row):
#         for j in range(col):
#             if grid[i][j] == "1" and (i, j) not in visit:
#                 ret += 1
#                 bfs(i, j)

#     return ret
