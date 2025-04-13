from abc import ABC, abstractmethod
from collections import deque
from typing import Callable, List


class IteratorInterface(ABC):
    @abstractmethod
    def hasNext(self) -> bool:
        """Return True if there are more elements to iterate over."""
        pass

    @abstractmethod
    def next(self):
        """Return the next element in the iteration."""
        pass


class ListIterator(IteratorInterface):
    def __init__(self, data: list):
        self.data = data
        self.index = 0

    def hasNext(self) -> bool:
        """Check if there are more elements in the list."""
        return self.index < len(self.data)

    def next(self):
        """Return the next element of the list and advance the index."""
        if self.hasNext():
            element = self.data[self.index]
            self.index += 1
            return element
        else:
            raise StopIteration("No more elements available")


class RangeIterator(IteratorInterface):
    def __init__(self, start: int, stop: int, step: int = 1):
        if step == 0:
            raise ValueError("Step cannot be zero.")
        self.curr = start
        self.stop = stop
        self.step = step

    def hasNext(self) -> bool:
        if self.step > 0:
            return self.curr < self.stop
        else:
            return self.curr > self.stop

    def next(self) -> int:
        if not self.hasNext():
            raise Exception("No more elements to iterate.")
        value = self.curr
        self.curr += self.step
        return value


class InterleaveIterator(IteratorInterface):
    def __init__(self, iterators: list):
        # Filter out any iterators that initially have no elements.
        self.iterators = deque([it for it in iterators if it.hasNext()])

    def hasNext(self) -> bool:
        # There is a next element if at least one iterator still has elements.
        return len(self.iterators) > 0

    def next(self):
        if not self.hasNext():
            raise StopIteration("No more elements available")
        # Pop the first iterator and retrieve its next element.
        curr_iter = self.iterators.popleft()
        res = curr_iter.next()
        # If the iterator still has elements, append it to the end.
        if curr_iter.hasNext():
            self.iterators.append(curr_iter)
        return res


class CycleIterator(IteratorInterface):
    def __init__(self, iterator: IteratorInterface):
        # Collect all elements from the given iterator.
        self.data = []
        while iterator.hasNext():
            self.data.append(iterator.next())
        if not self.data:
            raise ValueError("The provided iterator has no elements to cycle.")
        self.index = 0

    def hasNext(self) -> bool:
        # As long as there is at least one element, cycle indefinitely.
        return True

    def next(self):
        # Return the curr element and move index in a cyclic manner.
        element = self.data[self.index]
        self.index = (self.index + 1) % len(self.data)
        return element


class CycleIterator2(IteratorInterface):
    def __init__(self, iterator: IteratorInterface):
        self.iterator = iterator
        self.data = []  # Stores elements as they are lazily loaded.
        self.index = 0  # Points to the next element in the cycle.
        self.exhausted = (
            False  # Flag to indicate if the original iterator is exhausted.
        )

    def hasNext(self) -> bool:
        # If we have at least one element already stored or
        # if the original iterator isn't exhausted yet, we have a next element.
        return bool(self.data) or not self.exhausted

    def next(self):
        # First, try to pull from the original iterator if it is not exhausted.
        if not self.exhausted:
            if self.iterator.hasNext():
                element = self.iterator.next()
                self.data.append(element)
                return element
            else:
                # Mark the iterator as exhausted. If no element was ever added,
                # then raise an error because we have nothing to cycle.
                self.exhausted = True
                if not self.data:
                    raise ValueError("The provided iterator has no elements to cycle.")
        # At this point, the original iterator is exhausted.
        # Return the next element from the stored data in a cyclic manner.
        element = self.data[self.index]
        self.index = (self.index + 1) % len(self.data)
        return element


class FilterIterator(IteratorInterface):
    def __init__(self, iterator: IteratorInterface, func: Callable[[int], bool]):
        self.iterator = iterator
        self.func = func
        self.next_item = None
        self._advance()

    def _advance(self):
        self.next_item = None
        while self.iterator.hasNext():
            candidate = self.iterator.next()
            if self.func(candidate):
                self.next_item = candidate
                break

    def hasNext(self) -> bool:
        return self.next_item is not None

    def next(self):
        if not self.hasNext():
            raise StopIteration("No more elements available")
        result = self.next_item
        self._advance()
        return result


class FilteringIterator2(IteratorInterface):
    def __init__(self, arr: List[int], filter: Callable[[int], bool]):
        self.arr = arr
        self.filter = filter
        self.cur_idx = 0
        self.next_elem = None
        self._advance()  # Initialize the first valid element

    def _advance(self):
        self.next_elem = None
        while self.cur_idx < len(self.arr):
            candidate = self.arr[self.cur_idx]
            self.cur_idx += 1
            if self.filter(candidate):
                self.next_elem = candidate
                break

    def hasNext(self) -> bool:
        return self.next_elem is not None

    def next(self) -> int:
        if self.next_elem is None:
            raise Exception("No more elements that satisfy the filter.")
        result = self.next_elem
        self._advance()  # Move to the next valid element
        return result


if __name__ == "__main__":
    sample_list = [1, 2, 3, 4, 5]
    iterator = ListIterator(sample_list)

    while iterator.hasNext():
        print(iterator.next())
