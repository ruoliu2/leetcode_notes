from functools import cache
from math import inf


class Solution:
    @cache
    def numMaxChamberDFS(self, x, y, px, py):
        n, m = len(self.cave), len(self.cave[0])
        if x < 0 or y < 0 or x >= n or y >= m or self.cave[x][y] == "X":
            return -inf
        if x == n - 1 and y == m - 1:
            return 1
        cost_down = self.numMaxChamberDFS(x + 1, y, x, y) + 1
        cost_right = self.numMaxChamberDFS(x, y + 1, x, y) + 1 if y + 1 != py else -inf
        cost_left = self.numMaxChamberDFS(x, y - 1, x, y) + 1 if y - 1 != py else -inf
        cost = max(cost_down, cost_left, cost_right)
        return cost

    def numMaxChamber(self, cave):
        n, m = len(cave), len(cave[0])
        self.cave = cave
        cost = self.numMaxChamberDFS(0, 0, -1, -1)

        # If the cost is negative, return -1, otherwise return the cost
        return -1 if cost < 0 else cost


if __name__ == "__main__":
    cave = ["..X.", "...X", "....", "X..."]
    cave = [
        "......",
        ".XXXX.",
        "...X..",
        "...X.X",
        "......",
    ]

    print("Maximum number of chambers:", Solution().numMaxChamber(cave))
