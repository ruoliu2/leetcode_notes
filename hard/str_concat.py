class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        wlen = len(words[0])
        words_cnt = Counter(words)
        res = []
        wnd_cnt = collections.defaultdict(int)
        used_cnt = 0
        # iterate the string in with all possibility from length
        for i in range(wlen):
            start = i
            # reset wnd, and used word cnt
            wnd_cnt = collections.defaultdict(int)
            used_cnt = 0
            # iterate while, until hit end, interval wlen
            for i in range(start, len(s) - wlen + 1, wlen):
                cword = s[i:i+wlen]

                if cword not in words_cnt:
                    # clear wnd, reset used word cnt
                    start = i + wlen
                    used_cnt = 0
                    wnd_cnt = collections.defaultdict(int)
                    continue

                wnd_cnt[cword] += 1
                used_cnt += 1
                while wnd_cnt[cword] > words_cnt[cword]:
                    wnd_cnt[s[start:start+wlen]] -= 1
                    used_cnt -= 1
                    start += wlen

                # found the starting index we want to add
                if used_cnt == len(words):
                    res.append(start)
                    # dont need since need to account for every substring
                    # start += len(words) * wlen
                    # wnd_cnt = collections.defaultdict(int)
                    # used_cnt = 0
        return res
