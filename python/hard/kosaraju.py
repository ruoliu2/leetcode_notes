"""
https://www.baeldung.com/cs/kosaraju-algorithm-scc

SCC

1. DFS
2. build TG
3. DFS on TG

def dfs(g):


"""


import collections


def find_all_cycles(g, vs):
    """
    g: {node: [neis]}
    vs: [nodes]
    es: [(node, node)]
    """
    visited = set()
    st = []

    def dfs(cur):
        # dfs and mark priority of nodes
        for nei in g[cur]:
            if nei in visited:
                continue
            visited.add(nei)
            dfs(nei)
        st.append(cur)

    # make tg
    tg = collections.defaultdict(list)
    for v in vs:
        for nei in g[v]:
            tg[nei].append(v)

    res = []
    for v in vs:
        if v in visited:
            continue
        visited.add(v)
        dfs(v)
    # st has been populated with increasing priority of nodes
    visited = set()

    def pdfs(cur, cycle):
        for nei in tg[cur]:
            if nei in visited:
                continue
            visited.add(nei)
            cycle.add(nei)
            pdfs(nei, cycle)
        if len(cycle) > 1:
            res.append(cycle)
        return cycle

    # start with highest priority node
    while st:
        cur = st.pop()
        if cur in visited:
            continue
        # pdfs on tg
        pdfs(cur, set(cur))
        visited.add(cur)
    return res
