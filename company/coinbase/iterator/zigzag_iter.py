from collections import deque
from itertools import zip_longest
from typing import List, Generator, Optional
import unittest


class InterleaveIterator:
    def __init__(self, arr: List[List[int]], is_cycled: bool):
        self.arr = arr
        self.is_cycled = is_cycled
        self.q = deque()  # list_idx, element_idx
        self.reset()

    def hasNext(self) -> bool:
        if self.q:
            return True
        if not self.is_cycled:
            return False
        self.reset()
        return bool(self.q)

    def next(self) -> int:
        if not self.q:
            if not self.is_cycled:
                raise RuntimeError("No more elements")
            self.reset()
        l_idx, e_idx = self.q.popleft()
        if e_idx + 1 < len(self.arr[l_idx]):
            self.q.append((l_idx, e_idx + 1))
        return self.arr[l_idx][e_idx]

    def reset(self):
        for i, sublist in enumerate(self.arr):
            if sublist:
                self.q.append((i, 0))


class TestInterleaveIterator(unittest.TestCase):
    @staticmethod
    def stringifyResult(iterator: InterleaveIterator) -> str:
        result = []
        while iterator.hasNext():
            result.append(str(iterator.hasNext()))
            result.append(str(iterator.next()))
        result.append(str(iterator.hasNext()))
        return str(result)

    @staticmethod
    def stringifyResult_times(iterator: InterleaveIterator, times: int) -> str:
        result = []
        while iterator.hasNext() and times > 0:
            result.append(iterator.next())
            times -= 1
        return str(result)

    def test_cycled_iterator(self):
        arr1 = [[1, 2], [3], [4]]
        iterator1 = InterleaveIterator(arr1, True)

        expected = [1, 3, 4, 2, 1, 3, 4, 2, 1, 3]
        actual = []
        for _ in range(10):
            self.assertTrue(iterator1.hasNext())
            actual.append(iterator1.next())

        self.assertEqual(actual, expected)
        print()
        print(
            self.stringifyResult_times(InterleaveIterator(arr1, True), 10),
        )

    def test_non_cycled_iterator(self):
        arr2 = [[1, 2], [3, 4], [5, 6]]
        iterator2 = InterleaveIterator(arr2, False)

        expected_values = [1, 3, 5, 2, 4, 6]
        expected_has_next = [True] * 6 + [False]

        actual_values = []
        actual_has_next = []

        while iterator2.hasNext():
            actual_has_next.append(iterator2.hasNext())
            actual_values.append(iterator2.next())
        actual_has_next.append(iterator2.hasNext())

        self.assertEqual(actual_values, expected_values)
        self.assertEqual(actual_has_next, expected_has_next)
        print()
        print(self.stringifyResult(InterleaveIterator(arr2, False)))

    def test_uneven_lists_cycled(self):
        arr3 = [[1, 2], [3], [4, 5, 6, 7]]
        iterator3 = InterleaveIterator(arr3, True)

        expected = [1, 3, 4, 2, 5, 6, 7, 1, 3, 4, 2, 5]
        actual = []
        for _ in range(12):
            self.assertTrue(iterator3.hasNext())
            actual.append(iterator3.next())

        self.assertEqual(actual, expected)
        print()
        print(self.stringifyResult_times(InterleaveIterator(arr3, True), 12))

    def test_empty_lists(self):
        arr4 = [[], [], []]
        iterator4 = InterleaveIterator(arr4, False)

        self.assertFalse(iterator4.hasNext())

        iterator5 = InterleaveIterator(arr4, True)
        self.assertFalse(iterator5.hasNext())

    def test_some_empty_lists(self):
        arr5 = [[1, 2], [], [3, 4], []]
        iterator6 = InterleaveIterator(arr5, False)

        expected_values = [1, 3, 2, 4]
        actual_values = []

        while iterator6.hasNext():
            actual_values.append(iterator6.next())

        self.assertEqual(actual_values, expected_values)

    def test_single_element_lists(self):
        arr6 = [[1], [2], [3]]
        iterator7 = InterleaveIterator(arr6, False)

        expected_values = [1, 2, 3]
        actual_values = []

        while iterator7.hasNext():
            actual_values.append(iterator7.next())

        self.assertEqual(actual_values, expected_values)

    def test_exception_when_empty(self):
        arr7 = [[1], [2]]
        iterator8 = InterleaveIterator(arr7, False)

        # Consume all elements
        iterator8.next()
        iterator8.next()

        self.assertFalse(iterator8.hasNext())
        with self.assertRaises(RuntimeError):
            iterator8.next()


if __name__ == "__main__":
    unittest.main()
