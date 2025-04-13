import heapq
from typing import List


class CryptoMarket:
    def __init__(self, buyOrders: List[int], sellOrders: List[int]):
        self.buyOrdersHeap = [-price for price in buyOrders]
        self.sellOrdersHeap = sellOrders[:]
        heapq.heapify(self.buyOrdersHeap)
        heapq.heapify(self.sellOrdersHeap)

    def addOrder(self, price: int, orderType: str) -> float:
        if orderType == "sell":
            heapq.heappush(self.sellOrdersHeap, price)
        elif orderType == "buy":
            heapq.heappush(self.buyOrdersHeap, -price)

        # check match is present
        if len(self.buyOrdersHeap) > 0 and len(self.sellOrdersHeap) > 0:
            if -self.buyOrdersHeap[0] >= self.sellOrdersHeap[0]:
                # transaction happened
                sellPrice = heapq.heappop(self.sellOrdersHeap)
                buyPrice = -heapq.heappop(self.buyOrdersHeap)
                return (sellPrice + buyPrice) / 2.0
        return -1


# Example usage:
if __name__ == "__main__":
    # Example 1
    market = CryptoMarket([100, 100, 98, 99, 97], [109, 110, 110, 114, 115, 119])
    print(market.addOrder(200, "buy"))  # 154.5
    print(market.addOrder(105, "buy"))  # -1.0
    print(market.addOrder(100, "sell"))  # 102.5
    print(market.addOrder(130, "sell"))  # -1.0
