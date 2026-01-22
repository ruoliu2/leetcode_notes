"""
Letter Pairs (Affirm)

For each letter in the input words, find the other letter(s) that appear
in the most number of words together with that letter.

Example: ['abc', 'bcd', 'cde']
  a: [b, c]   # b,c each appear in 1 word with a
  b: [c]      # c appears in 2 words with b (abc, bcd); a,d only 1 each
  c: [b, d]   # b,d each appear in 2 words with c; a,e only 1 each
  d: [c]      # c appears in 2 words with d (bcd, cde); b,e only 1 each
  e: [c, d]   # c,d each appear in 1 word with e

Approach:
  1. For each word, count co-occurrences of all letter pairs
  2. For each letter, find which other letters have max co-occurrence count
"""
from collections import defaultdict


def find_top_pairs(words: list[str]) -> dict[str, list[str]]:
    # Count co-occurrences: pair_count[a][b] = # words containing both a and b
    pair_count = defaultdict(lambda: defaultdict(int))

    for word in words:
        chars = set(word)  # unique chars in this word
        for c1 in chars:
            for c2 in chars:
                if c1 != c2:
                    pair_count[c1][c2] += 1

    # For each letter, find other letters with max count
    result = {}
    for c1, counts in pair_count.items():
        max_count = max(counts.values())
        result[c1] = sorted([c2 for c2, cnt in counts.items() if cnt == max_count])

    return result


if __name__ == "__main__":
    words = ["abc", "bcd", "cde"]
    result = find_top_pairs(words)
    for k, v in sorted(result.items()):
        print(f"{k}: {v}")
    # a: ['b', 'c']
    # b: ['c']
    # c: ['b', 'd']
    # d: ['c']
    # e: ['c', 'd']
