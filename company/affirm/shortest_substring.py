"""
Shortest Uncommon Substring (Affirm / LC 3076)

For each arr[i], find shortest substring not occurring in any other string.
If tie, return lexicographically smallest.

Example: ["cheapair","cheapoair","peloton","pelican"]
Output:  ["pa", "po", "t", "ca"]
  - "cheapair": "pa" (length-2, others have overlapping 1-2 char substrings)
  - "cheapoair": "po" ("oa" also valid)
  - "peloton": "t" (single char unique)
  - "pelican": "ca" ("li","ic","an" also valid)

Approach (Trie):
  1. Build Trie of all substrings, track which string indices have each
  2. For each string, check substrings by (length ASC, lex ASC)
  3. Return first where only current index has it

Follow-up 1: Optimize substr() -> iterate by length (already done)
Follow-up 2: If no unique exists, return shortest with fewest occurrences
"""


class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, s: str, idx: int):
        """Insert all substrings of s, mark with string index."""
        for i in range(len(s)):
            cur = self.root
            for j in range(i, len(s)):
                c = s[j]
                if c not in cur:
                    cur[c] = {"#": set()}
                cur = cur[c]
                cur["#"].add(idx)

    def find_unique(self, s: str, idx: int) -> str:
        """Find shortest substring of s that only belongs to idx."""
        n = len(s)
        for length in range(1, n + 1):
            candidates = []
            for i in range(n - length + 1):
                sub = s[i : i + length]
                if self._only_in(sub, idx):
                    candidates.append(sub)
            if candidates:
                return min(candidates)
        return ""

    def find_rarest(self, s: str, idx: int) -> str:
        """Follow-up 2: Find shortest substring with fewest occurrences."""
        n = len(s)
        for length in range(1, n + 1):
            best_sub, best_count = "", float("inf")
            for i in range(n - length + 1):
                sub = s[i : i + length]
                count = self._count(sub)
                if count < best_count or (count == best_count and sub < best_sub):
                    best_sub, best_count = sub, count
            if best_count == 1:  # unique found
                return best_sub
        return best_sub  # return rarest at max length

    def _only_in(self, sub: str, idx: int) -> bool:
        cur = self.root
        for c in sub:
            if c not in cur:
                return True
            cur = cur[c]
        return cur["#"] == {idx}

    def _count(self, sub: str) -> int:
        cur = self.root
        for c in sub:
            if c not in cur:
                return 0
            cur = cur[c]
        return len(cur["#"])


class Solution:
    def shortestSubstrings(self, arr: list[str]) -> list[str]:
        trie = Trie()
        for i, s in enumerate(arr):
            trie.insert(s, i)
        return [trie.find_unique(s, i) for i, s in enumerate(arr)]


if __name__ == "__main__":
    sol = Solution()
    print(sol.shortestSubstrings(["cheapair", "cheapoair", "peloton", "pelican"]))
    # ['pa', 'po', 't', 'ca'] or ['pa', 'oa', 't', 'li'] etc

    print(sol.shortestSubstrings(["cab", "ad", "bad", "c"]))
    # ['ab', '', 'ba', '']

    print(sol.shortestSubstrings(["abc", "bcd", "abcd"]))
    # ['', '', 'abcd']
