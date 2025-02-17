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
        if arr[m] <= target:
            l = m + 1
        else:
            r = m
    return l


# finds the rightmost (largest) index i in the array such that
# the element arr[i] is less than or equal to target
# if no such index exists, returns 0 not -1
def bisect_right_find_max(arr, target):  # right biased
    l, r = 0, len(arr) - 1
    while l < r:
        m = (l + r + 1) // 2
        if arr[m] <= target:
            l = m
        else:
            r = m - 1
    return l
