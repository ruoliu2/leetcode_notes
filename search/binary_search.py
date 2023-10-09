def binSearch(nums, target):
    l, r = 0, len(nums) - 1
    while l <= r:
        m = (l + r) // 2
        if nums[m] < target:
            l = m + 1
        elif nums[m] > target:
            r = m - 1
        else:
            return m
    return -1


def bisect_left(arr, target):
    l, r = 0, len(arr)
    while l < r:
        m = (l + r) // 2
        if arr[m] < target:
            l = m + 1
        else:
            r = m
    return l


def bisect_right(arr, target):
    l, r = 0, len(arr)
    while l < r:
        m = (l + r) // 2
        if arr[m] > target:
            r = m
        else:
            l = m + 1
    return l
