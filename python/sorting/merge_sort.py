def merge(arr, s, m, e):
    # Copy the sorted left & right halfs to temp arrays
    l, r = arr[s : m + 1], arr[m + 1 : e + 1]
    i = j = 0  # index for l & r
    k = s  # index for arr
    while i < len(l) and j < len(r):  # merge two sorted halfs
        if l[i] <= r[j]:
            arr[k] = l[i]
            i += 1
        else:
            arr[k] = r[j]
            j += 1
        k += 1
    # one of the two will have remaining
    if i < len(l):
        arr[k:] = l[i:]
    else:
        arr[k:] = r[j:]


def merge_sort(arr, s, e):
    if e <= s:
        return arr
    m = (s + e) // 2
    merge_sort(arr, s, m)
    merge_sort(arr, m + 1, e)
    merge(arr, s, m, e)
    return arr
