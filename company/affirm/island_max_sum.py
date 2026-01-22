"""
Sum of Islands Max (Affirm)

Given m x n grid with positive integers (land) and 0 (water),
find sum of the max value from each island.

Example: [[0,2,0,0],[3,4,0,5],[0,0,0,6],[7,0,8,0]]
  Islands: [2,3,4]->4, [5,6]->6, [7]->7, [8]->8
  Output: 4 + 6 + 7 + 8 = 25

Approach: DFS each island, track max, sum all maxes.
"""


def sum_island_max(grid: list[list[int]]) -> int:
    if not grid:
        return 0

    m, n = len(grid), len(grid[0])
    visited = [[False] * n for _ in range(m)]

    def dfs(i: int, j: int) -> int:
        if i < 0 or i >= m or j < 0 or j >= n:
            return 0
        if visited[i][j] or grid[i][j] == 0:
            return 0

        visited[i][j] = True
        max_val = grid[i][j]
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            max_val = max(max_val, dfs(i + di, j + dj))
        return max_val

    total = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] > 0 and not visited[i][j]:
                total += dfs(i, j)

    return total


if __name__ == "__main__":
    grid1 = [[0, 2, 0, 0], [3, 4, 0, 5], [0, 0, 0, 6], [7, 0, 8, 0]]
    print(sum_island_max(grid1))  # 25

    grid2 = [[1, 0, 2], [0, 3, 0], [4, 0, 5]]
    print(sum_island_max(grid2))  # 15 (1+2+3+4+5, each is own island)

    grid3 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    print(sum_island_max(grid3))  # 0
