class Solution:
    def ladderLength(self, start_word: str, end_word: str, word_list: List[str]) -> int:
        if end_word not in word_list:
            return 0
        # build word graph
        word_list = set(word_list)
        word_list.add(start_word)

        # p*g - [list of words in this pattern]
        g = defaultdict(set)
        for word in word_list:
            for i in range(len(word)):
                pattern = word[:i] + "*" + word[i + 1:]
                g[pattern].add(word)

        visit = set([start_word])

        def neis(word):
            for i in range(len(word)):
                pattern = word[:i] + "*" + word[i + 1:]
                for nei in g[pattern]:
                    if nei not in visit:
                        visit.add(nei)
                        yield nei

        # bfs
        res = 1
        q = deque([start_word])
        while q:
            for i in range(len(q)):
                cur = q.popleft()
                if cur == end_word:
                    return res
                for nei in neis(cur):
                    q.append(nei)
            res += 1
        return 0
