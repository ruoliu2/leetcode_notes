from collections import defaultdict, deque
from typing import List

"""
https://www.baeldung.com/cs/dag-topological-sort

recursive:

def topsort(G):
    mark all nodes u as visited
    T = {}
    time = 0
    while there is unvisited node u do:
        dfs(u)
    output T 
    
    # the post-ordring sort should be topsort result 
    # root is largest
    
def dfs(u):
    mark u as visited
    pre(u) = ++ time
    for each edge (u, v) in Out(u):
        if v is not visited:
            add edge (u, v) to T
            dfs(v)
    post(u) = ++ time

time: (m+n)
"""

"""
iterative: (Kahn's)

def topsort(g):
    compute inDegree for v in g
    put all v in q
    l = []
    while q:
        remove u from q
        l.append(u)
        for nei in g[u]:
            decrease nei inDegree by 1
            if inDegree[v] == 0:
                add v to q 
    return l

"""

# topsort + bfs


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        inDeg = defaultdict(int)
        pre = defaultdict(list)
        for n1, n2 in prerequisites:
            inDeg[n2] += 1
            pre[n1].append(n2)

        zeroDeg = [i for i in range(numCourses) if inDeg[i] == 0]
        visit = len(zeroDeg)
        q = deque(zeroDeg)
        while q:
            cur = q.popleft()
            for nei in pre[cur]:
                inDeg[nei] -= 1
                if inDeg[nei] == 0:
                    visit += 1
                    q.append(nei)
        return visit == numCourses


def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
    n = len(colors)
    indegrees = [0] * n
    graph = defaultdict(list)
    for s, d in edges:
        graph[s].append(d)
        indegrees[d] += 1
    zero_indegrees = deque([i for i in range(n) if indegrees[i] == 0])
    cnt = [[0] * 26 for i in range(n)]

    visit = res = 0
    while zero_indegrees:
        node = zero_indegrees.popleft()
        cnt[node][ord(colors[node]) - ord("a")] += 1
        visit += 1
        for nei in graph[node]:
            for c in range(26):
                cnt[nei][c] = max(cnt[nei][c], cnt[node][c])
            indegrees[nei] -= 1
            if indegrees[nei] == 0:
                zero_indegrees.append(nei)
        res = max(res, max(cnt[node]))

    return res if visit == n else -1
