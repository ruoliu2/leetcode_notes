from typing import List
import heapq


class transaction:
    def __init__(self, amount: int, price: float):
        self.amount = amount
        self.price = price


class Solution:
    def __init__(self):
        self.buy_heap = []
        self.total_tax = 0.0

    def buy(self, amount: int, price: float):
        heapq.heappush(self.buy_heap, (-price, transaction(amount, price)))

    def sell(self, amount: int, price: float):
        remaining = amount
        while remaining > 0 and self.buy_heap:
            neg_price, top_buy = heapq.heappop(self.buy_heap)
            sell_amount = min(remaining, top_buy.amount)
            profit = (price - top_buy.price) * sell_amount
            if profit > 0:
                self.total_tax += 0.1 * profit
            remaining -= sell_amount
            if top_buy.amount > 0:
                heapq.heappush(self.buy_heap, (-top_buy.price, top_buy))

    def calculateMinimalTax(self, transactions: List[List[str]]) -> float:
        # Priority queue to store buy transactions sorted by price descending

        for record in transactions:
            txn_type = record[1]
            amount = int(record[2])
            price = float(record[3])

            if txn_type == "buy":
                self.buy(amount, price)
            else:
                self.sell(amount, price)

        return self.total_tax
