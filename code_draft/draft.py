from collections import defaultdict
from functools import cache


class Solution:
    def shortestPath(self, words, k):
        # make bitmap (set) for every word, store cnt for each bitmap
        wordCnt = defaultdict(int)
        for word in words:
            bitmap = 0
            for ch in word:
                bitmap |= 1 << (ord(ch) - ord('a'))
            wordCnt[bitmap] += 1

        @cache
        def dp(n, bitmap):  # dp for to get how many words you can make
            res = 0
