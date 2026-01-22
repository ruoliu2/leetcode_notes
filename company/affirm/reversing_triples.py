"""
Count Reversing Triples (Affirm / LC 334 variant)

Count triplets (i, j, k) where i < j < k and nums[i] > nums[j] > nums[k].

Example: [4, 1, 5, 3, 2] -> 2
  Triplets: [4,3,2], [5,3,2]

Approach: For each middle j, count:
  - left: elements on left > nums[j]
  - right: elements on right < nums[j]
  - contribution: left * right

O(n²) solution: simple nested loops
O(n log n) solution: precompute with SortedList + binary search
"""
from bisect import bisect_left, bisect_right


def count_reversing_triples(nums: list[int]) -> int:
    """O(n²) - simple and clean."""
    n = len(nums)
    total = 0
    for j in range(1, n - 1):
        left = sum(1 for i in range(j) if nums[i] > nums[j])
        right = sum(1 for k in range(j + 1, n) if nums[k] < nums[j])
        total += left * right
    return total


def count_reversing_triples_optimized(nums: list[int]) -> int:
    """O(n log n) using precomputed arrays + binary search."""
    from sortedcontainers import SortedList  # pip install sortedcontainers

    n = len(nums)
    if n < 3:
        return 0

    # Precompute left_greater[j] = count of nums[i] > nums[j] for i < j
    left_greater = [0] * n
    left_list = SortedList()
    for j in range(n):
        # Count elements > nums[j] = total - count of elements <= nums[j]
        left_greater[j] = len(left_list) - left_list.bisect_right(nums[j])
        left_list.add(nums[j])

    # Precompute right_smaller[j] = count of nums[k] < nums[j] for k > j
    right_smaller = [0] * n
    right_list = SortedList()
    for j in range(n - 1, -1, -1):
        # Count elements < nums[j]
        right_smaller[j] = right_list.bisect_left(nums[j])
        right_list.add(nums[j])

    # Sum contributions
    return sum(left_greater[j] * right_smaller[j] for j in range(1, n - 1))


if __name__ == "__main__":
    tests = [[4, 1, 5, 3, 2], [5, 4, 3, 2, 1], [2, 4, 1, 3, 5]]
    expected = [2, 10, 0]

    print("=== O(n²) ===")
    for t, e in zip(tests, expected):
        print(f"{t} -> {count_reversing_triples(t)} (expected {e})")

    print("\n=== O(n log n) ===")
    for t, e in zip(tests, expected):
        print(f"{t} -> {count_reversing_triples_optimized(t)} (expected {e})")
