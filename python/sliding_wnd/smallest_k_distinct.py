from collections import defaultdict


def smallest_subarray_with_k_distinct(arr, k):
    l, res, distinct_cnt = 0, float("inf"), 0
    freq = defaultdict(int)
    for r, val in enumerate(arr):
        if freq[val] == 0:
            distinct_cnt += 1
        freq[val] += 1
        while distinct_cnt == k:
            res = min(res, r - l + 1)
            freq[arr[l]] -= 1
            if freq[arr[l]] == 0:
                distinct_cnt -= 1
            l += 1
    return res if res != float("inf") else -1
