def bucketSort(arr):
    # Assuming arr only contains 0, 1 or 2
    counts = [0, 0, 0]

    # Count the quantity of each val in arr
    for i in arr:
        counts[i] += 1

    # Fill each bucket in the original array
    p = 0
    for i, count in enumerate(counts):
        for _ in range(count):
            arr[p] = i
            p += 1
    return arr
