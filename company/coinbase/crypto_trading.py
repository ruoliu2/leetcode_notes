from enum import Enum, auto
from typing import Dict, List, Optional


class State(Enum):
    LIVE = auto()
    PAUSED = auto()
    COMPLETED = auto()
    CANCELED = auto()


class Order:
    def __init__(self, id: str, currency: str, amount: int, timestamp: int, type: str):
        self.id = id
        self.currency = currency
        self.amount = amount
        self.timestamp = timestamp
        self.type = type
        self.state = State.LIVE

    def __str__(self):
        return f"Order(id={self.id}, currency={self.currency}, amount={self.amount}, timestamp={self.timestamp}, type={self.type}, state={self.state})"


class CryptoTradingSystem:
    def __init__(self):
        self.order_map: Dict[State, Dict[str, Order]] = {
            State.LIVE: {},
            State.PAUSED: {},
            State.COMPLETED: {},
            State.CANCELED: {},
        }

    def placeOrder(
        self, id: str, currency: str, amount: int, timestamp: int, type: str
    ) -> str:
        if self._findOrder(id) is not None:
            return ""
        order = Order(id, currency, amount, timestamp, type)
        self.order_map[State.LIVE][id] = order
        return id

    def pauseOrder(self, id: str) -> str:
        order = self.order_map[State.LIVE].pop(id, None)
        if order is None:
            return ""
        order.state = State.PAUSED
        self.order_map[State.PAUSED][id] = order
        return id

    def resumeOrder(self, id: str) -> str:
        order = self.order_map[State.PAUSED].pop(id, None)
        if order is None:
            return "Order is not paused"
        order.state = State.LIVE
        self.order_map[State.LIVE][id] = order
        return id

    def cancelOrder(self, id: str) -> str:
        currentState = self._getOrderState(id)
        if (
            currentState is None
            or currentState == State.COMPLETED
            or currentState == State.CANCELED
        ):
            return ""
        order = self.order_map[currentState].pop(id, None)
        if order is None:
            return ""
        order.state = State.CANCELED
        self.order_map[State.CANCELED][id] = order
        return id

    def completeOrder(self, id: str) -> str:
        if id in self.order_map[State.COMPLETED]:
            return "Order is already completed"
        order = self.order_map[State.LIVE].pop(id, None)
        if order is None:
            return "Order is not live"
        order.state = State.COMPLETED
        self.order_map[State.COMPLETED][id] = order
        return id

    def displayLiveOrders(self) -> List[str]:
        liveOrders = list(self.order_map[State.LIVE].values())
        liveOrders.sort(key=lambda o: o.timestamp)
        orderIds = []
        for order in liveOrders:
            orderIds.append(order.id)
        return orderIds

    def _findOrder(self, id: str) -> Optional[Order]:
        for orders in self.order_map.values():
            if id in orders:
                return orders[id]
        return None

    def _getOrderState(self, id: str) -> Optional[State]:
        for st, orders in self.order_map.items():
            if id in orders:
                return st
        return None


if __name__ == "__main__":
    system = CryptoTradingSystem()

    print(system.placeOrder("order-1", "BTC", 100, 1, "buy"))  # Output: "order-1"
    print(system.placeOrder("order-2", "ETH", 50, 2, "sell"))  # Output: "order-2"
    print(system.placeOrder("order-3", "BNB", 30, 3, "buy"))  # Output: "order-3"

    print(system.pauseOrder("order-1"))  # Output: "order-1"
    print(system.displayLiveOrders())  # Output: ["order-2", "order-3"]

    print(system.resumeOrder("order-1"))  # Output: "order-1"
    print(system.resumeOrder("order-2"))  # Output: "" (order-2 is not paused)

    print(system.cancelOrder("order-2"))  # Output: "order-2"
    print(system.completeOrder("order-3"))  # Output: "order-3"
    print(system.completeOrder("order-3"))  # Output: "" (order-3 already completed)

    print(system.displayLiveOrders())  # Output: ["order-1"]
