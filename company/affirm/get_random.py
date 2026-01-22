"""
Random Dictionary (Affirm)

Design a dictionary supporting O(1) for all operations:
  - get(key)
  - put(key, val)
  - delete(key)
  - get_random_val() - unique values with equal probability

Example: {a:5, b:5, c:6, d:5}
  get_random_val() -> 5 with prob 1/2, 6 with prob 1/2

Core Logic (LC 381 pattern):
  - map: key -> val (standard dict)
  - lst: list of unique vals (for O(1) random.choice)
  - idx: val -> set of indices in lst (for O(1) swap-with-last removal)
  - cnt: val -> count of keys with this val

  On put/delete:
    - cnt 0->1: add val to lst, record index in idx
    - cnt 1->0: swap-with-last removal from lst, update idx
"""
import random
from collections import defaultdict


class RandomDict:
    """
    O(1) get/put/delete/get_random. Adapted from LC 381 pattern.

    Key insight: maintain list of UNIQUE vals for random.choice().
    When val count 0->1: append to list. When 1->0: swap-with-last removal.
    """

    def __init__(self):
        self.map = {}                # key -> val
        self.lst = []                # unique vals
        self.idx = defaultdict(set)  # val -> set of indices in lst (size 0 or 1)
        self.cnt = defaultdict(int)  # val -> count of keys with this val

    def get(self, key):
        return self.map.get(key)

    def put(self, key, val):
        if key in self.map:
            self._remove_val(self.map[key])
        self.map[key] = val
        self._add_val(val)

    def delete(self, key):
        if key in self.map:
            self._remove_val(self.map.pop(key))

    def get_random_val(self):
        return random.choice(self.lst)

    def _add_val(self, val):
        self.cnt[val] += 1
        if self.cnt[val] == 1:  # first occurrence, add to lst
            self.idx[val].add(len(self.lst))
            self.lst.append(val)

    def _remove_val(self, val):
        self.cnt[val] -= 1
        if self.cnt[val] == 0:  # last occurrence, remove from lst
            # swap-with-last
            remove, last = self.idx[val].pop(), self.lst[-1]
            self.lst[remove] = last
            self.idx[last].add(remove)
            self.idx[last].discard(len(self.lst) - 1)
            self.lst.pop()


if __name__ == "__main__":
    d = RandomDict()
    for k, v in [("a", 5), ("b", 5), ("c", 6), ("d", 5)]:
        d.put(k, v)

    # Test: unique vals with equal probability
    counts = {5: 0, 6: 0}
    for _ in range(1000):
        counts[d.get_random_val()] += 1
    print(f"Counts: {counts}")  # ~500 for 5, ~500 for 6
