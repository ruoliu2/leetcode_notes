class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        """
        Monotonic stack solution.
        For each bar, we find the widest range where it is the minimum height.
        """
        max_area = 0
        st: list[tuple[int, int]] = []  # (start_index, height)

        for i, height in enumerate(heights):
            start = i
            # Pop higher bars and finalize their max area
            while st and st[-1][1] > height:
                prev_start, prev_height = st.pop()
                width = i - prev_start
                max_area = max(max_area, prev_height * width)
                start = prev_start  # extend current bar back to earliest start
            st.append((start, height))

        # Finalize areas for bars left in stack (extend to end of array)
        n = len(heights)
        for start, height in st:
            width = n - start
            max_area = max(max_area, height * width)

        return max_area