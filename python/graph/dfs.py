# 210 dfs with cycle & append only after dependency
from typing import List


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        g = [set() for i in range(numCourses)]
        for a, b in prerequisites:
            g[a].add(b)
        visit = set()
        path = set()
        res = []

        def dfs(node):
            if node in path:
                return False
            if node in visit:
                return True
            path.add(node)
            for nei in g[node]:
                if not dfs(nei):
                    return False
            path.discard(node)
            visit.add(node)
            res.append(node)
            return True

        for i in range(numCourses):
            if not dfs(i):
                return []
        return res
