from collections import defaultdict
from typing import List


class CurrencyConverter:
    def __init__(self, fromArr: List[str], toArr: List[str], rateArr: List[float]):
        # Constructor to initialize the currency graph
        self.g = defaultdict(list)
        n = len(fromArr)
        for i in range(n):
            from_currency = fromArr[i]
            to_currency = toArr[i]
            rate = rateArr[i]
            self.g[from_currency].append((to_currency, rate))
            self.g[to_currency].append((from_currency, 1 / rate))

    def getBestRate(self, from_: str, to: str) -> float:
        if from_ not in self.g or to not in self.g:
            return -1

        visited = set()
        return self.dfs(from_, to, 1, visited)

    def dfs(self, current: str, target: str, rate: float, visited: set) -> float:
        if current == target:
            return rate

        visited.add(current)
        max_rate = -1

        for to_currency, r in self.g[current]:
            if to_currency in visited:
                continue

            res = self.dfs(to_currency, target, rate * r, visited)
            max_rate = max(max_rate, res)

        visited.remove(current)
        return max_rate
