def minOperations(self, A: str, B: str) -> int:
    def findLength(nums1, nums2) -> int:
        n, m = len(nums1), len(nums2)
        # dp(i, j) means lcs in nums1[:i], nums2[:j]
        # We only need two rows: previous row (prev) and current row (curr)
        prev = [0] * (m + 1)
        curr = [0] * (m + 1)
        ans = 0

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if nums1[i - 1] == nums2[j - 1]:
                    curr[j] = prev[j - 1] + 1
                    ans = max(ans, curr[j])
                else:
                    curr[j] = 0
            # Move current row to previous row for the next iteration
            prev, curr = curr, prev

        return ans

    common = lcs(A, B)
    return len(A) + len(B) - 2 * common
