from typing import List


class Solution:
    def interleave(self, arr: List[List[int]]) -> List[int]:
        max_len = max(len(sublist) for sublist in arr)
        res = []
        for i in range(max_len):
            for sublist in arr:
                if i < len(sublist):
                    res.append(sublist[i])
        return res


if __name__ == "__main__":
    sol = Solution()
    print(sol.interleave([[1, 2, 3], [4], [7, 8]]))
