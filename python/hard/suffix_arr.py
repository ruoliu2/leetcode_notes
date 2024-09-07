def build_suffix_array(s):
    """
    Build and return the suffix array of the string s.
    The suffix array is a list of integers representing the starting
    indices of the suffixes of the string, sorted in lexicographical order.
    """
    return sorted(range(len(s)), key=lambda i: s[i:])


def build_lcp(s, suffix_arr):
    """
    Build and return the LCP (longest common prefix) array of the string s
    given its suffix array.
    """
    n = len(s)
    rank = [0] * n
    lcp = [0] * n

    # Create rank array where rank[i] gives the rank of suffix starting at index i
    for i, suffix in enumerate(suffix_arr):
        rank[suffix] = i

    h = 0
    for i in range(n):
        if rank[i] > 0:
            j = suffix_arr[rank[i] - 1]
            while i + h < n and j + h < n and s[i + h] == s[j + h]:
                h += 1
            lcp[rank[i]] = h
            if h > 0:
                h -= 1

    return lcp


def longest_repeating_substring(s):
    if not s:
        return 0

    # Step 1: Build the suffix array
    suffix_arr = build_suffix_array(s)

    # Step 2: Build the LCP array
    lcp = build_lcp(s, suffix_arr)

    # Step 3: The length of the longest repeating substring is the maximum value in the LCP array
    return max(lcp) if lcp else 0


# Example Usage:
s = "banana"
print(
    longest_repeating_substring(s)
)  # Output: 3 ("ana" is the longest repeating substring)
