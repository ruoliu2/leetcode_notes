# Mountain Rainfall
# Overview

# We want to write a program that determines the
# collection points of rain falling on mountainous terrain.

# One centimeter of rain falls uniformly across a mountain.
# Water flows downhill until it reaches a local minimum.
# Steepest descent, ties break in any way

# Input Specification

# You receive a 2-dimensional array of integers. The integer
# at position (x,y) in the array represents the elevation
# (in kilometers) of the terrain at position (x,y).

# Sample Input:
# [
#   [3, 3, 1, -1],
#   [2, 3, 3, 1],
#   [0, 1, 3, 3]
# ]

# Sample output:
# [
#   [0, 0, 0, 6],
#   [0, 0, 0, 0],
#   [6, 0, 0, 0]
# ]
# OR
# [
#   [0, 0, 0, 7],
#   [0, 0, 0, 0],
#   [5, 0, 0, 0]
# ]

from functools import cache
from itertools import product

def rainfall(heights: list[list[int]]) -> list[list[int]]:
    """
    Find the local minimum that water from (i, j) flows to.
    """
    n, m = len(heights), len(heights[0])
    res = [[0] * m for _ in range(n)]
    inbound = set(product(range(n), range(m)))
    accumulated = set()

    def neis(i, j):
        return {(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)} & inbound

    @cache
    def find_local_min(i, j):
        ri, rj = i, j
        for ni, nj in neis(i, j):
            if heights[ni][nj] < heights[i][j]:
                ri, rj = find_local_min(ni, nj)
                break
        if (i, j) not in accumulated:
            res[ri][rj] += 1
        accumulated.add((i, j))
        return (ri, rj)

    for i in range(n):
        for j in range(m):
            if (i, j) not in accumulated:
                find_local_min(i, j)

    return res


test_heights = [[3, 3, 1, -1], [2, 3, 3, 1], [0, 1, 3, 3]]

for height in rainfall(test_heights):
    print(height)
