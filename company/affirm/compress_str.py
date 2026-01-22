"""
String Compression (Affirm / LC 3163)

Compress: consecutive chars -> count + char (max count 9)
Decompress: reverse the process

Example:
  compress("aaabbc") -> "3a2b1c"
  compress("aaaaaaaaaaab") -> "9a2a1b"  (max 9 per group)
  decompress("3a2b1c") -> "aaabbc"
"""


def compress(word: str) -> str:
    if not word:
        return ""
    res, cnt, ch = "", 1, word[0]
    for i in range(1, len(word)):
        if word[i] == ch and cnt < 9:
            cnt += 1
        else:
            res += str(cnt) + ch
            ch, cnt = word[i], 1
    return res + str(cnt) + ch


def decompress(s: str) -> str:
    return "".join(s[i + 1] * int(s[i]) for i in range(0, len(s), 2))


if __name__ == "__main__":
    print(compress("aaabbc"))          # "3a2b1c"
    print(compress("aaaaaaaaaaab"))    # "9a2a1b"
    print(decompress("3a2b1c"))        # "aaabbc"
    print(decompress("9a2a1b"))        # "aaaaaaaaaaab"

    # Round-trip test
    original = "aaabbbccccdddddeeeee"
    assert decompress(compress(original)) == original
    print("Round-trip OK")
