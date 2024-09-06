def min_to_remove(arr, capacity):
    n = len(arr)
    idxs = [-1] * n
    for i, val in enumerate(arr):
        idxs[i] = bisect_right(arr, val * 3)
    res = n
    for i in range(n):
        res = min(res, i + n - idxs[i])
    return res
