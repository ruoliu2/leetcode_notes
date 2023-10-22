from collections import defaultdict
from collections import deque


# Compute the exchange rate
def maxAmountofExchange(exchanges: list[str], from_currency, to_currency):
    graph = defaultdict(list)
    for src, des, weight in exchanges:
        graph[src].append((des, float(weight)))
        graph[des].append((src, 1.0/float(weight)))

    rate = [-1.0]

    # DFS Iterative
    def dfs_iter(src, des):
        rate = -1.0
        if src not in graph or des not in graph:
            return rate
        stack = [(src, 1.0)]
        visited = set([src])
        while stack:
            currency, exch = stack.pop()
            if currency == des:
                rate = max(rate, exch)
            for neighbor, weight in graph[currency]:
                if neighbor not in visited:
                    stack.append((neighbor, exch * weight))
                    visited.add(neighbor)
        return rate

    # DFS recursive
    visited = set([from_currency])

    def dfs(src, des, exch):
        if src not in graph or des not in graph:
            return
        if src == des:
            rate[0] = max(rate[0], exch)
            return
        for neighbor, weight in graph[src]:
            if neighbor not in visited:
                visited.add(src)
                dfs(neighbor, des, exch * weight)

    # BFS doesn't work because it goes level by level and once we hit
    # the currency we want to exchange the value to we can't go any further
    def bfs(src, des):
        rate = -1.0
        if src not in graph or des not in graph:
            return rate
        queue = deque([(src, 1.0)])
        visited = set([src])
        while queue:
            currency, exch = queue.popleft()
            if currency == des:
                rate = max(rate, exch)
            for neighbor, weight in graph[currency]:
                if neighbor not in visited:
                    queue.append((neighbor, exch * weight))
                    visited.add(neighbor)
        return rate

    dfs(from_currency, to_currency, 1.0)
    return rate[0]


# another problem prereq list
def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    # dfs
    preMap = {i: [] for i in range(numCourses)}

    # map each course to : prereq list
    for crs, pre in prerequisites:
        preMap[crs].append(pre)

    visiting = set()

    def dfs(crs):
        if crs in visiting:
            return False
        if preMap[crs] == []:
            return True

        visiting.add(crs)
        for pre in preMap[crs]:
            if not dfs(pre):
                return False
        visiting.remove(crs)
        preMap[crs] = []
        return True

    for c in range(numCourses):
        if not dfs(c):
            return False
    return True
