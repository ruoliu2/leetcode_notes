nums = []
k = 0


def quick_sort(l, r):
    if r < l:
        return
    pivot, p = nums[r], l
    # Partition: elements smaller than pivot on left side
    for i in range(l, r):
        if nums[i] < pivot:
            nums[p], nums[i] = nums[i], nums[p]
            p += 1
    # Move pivot in-between left & right sides
    nums[p], nums[r] = nums[r], nums[p]
    quick_sort(l, p - 1)  # Quick sort left side
    quick_sort(p + 1, r)  # Quick sort right side


def quick_select(l, r):
    if r < l:
        return
    pivot, p = nums[r], l
    for i in range(l, r):
        if nums[i] < pivot:
            nums[p], nums[i] = nums[i], nums[p]
            p += 1
    nums[p], nums[r] = nums[r], nums[p]
    if p > k:
        quick_select(l, p - 1)
    elif p < k:
        quick_select(p + 1, r)
