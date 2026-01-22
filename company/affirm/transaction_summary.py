"""
Transaction Summary (Affirm)

Given List[Transaction] from CSV files, compute:
  Map[merchantId, Map[hourDiff, sumAmount]]

Rules:
  - Only COMPLETED transactions (use given Status enum)
  - Only last 24 hours
  - Group by merchantId and hour difference from current time
  - Sum amounts per group
  - Use given get_hour_diff() function

Follow-up (Production optimization):
  1. Database layer:
     - Pre-aggregate hourly rollups (materialized view)
     - Index on (status, startTime, merchantId)
     - Partition by time for faster range queries

  2. Caching:
     - Cache results with short TTL (e.g., 1 min)
     - Invalidate on new transactions

  3. Streaming:
     - Use Kafka/Flink for real-time aggregation
     - Maintain rolling 24h window incrementally
     - Avoid full scan on every query

  4. Query optimization:
     - Pre-filter COMPLETED in DB query
     - Only fetch last 24h data, not all history
"""

from collections import defaultdict
from enum import Enum
from dataclasses import dataclass


class Status(Enum):
    COMPLETED = "COMPLETED"
    PENDING = "PENDING"
    FAILED = "FAILED"


@dataclass
class Transaction:
    amount: int
    merchantId: str
    status: Status
    userId: str
    startTime: int  # timestamp in hours or seconds


def get_hour_diff(current_time: int, transaction_time: int) -> int:
    """Given function - calculates hour difference."""
    return current_time - transaction_time


def summarize_transactions(
    transactions: list[Transaction],
    current_time: int,
) -> dict[str, dict[int, int]]:
    """
    Returns: {merchantId: {hourDiff: sumAmount}}
    Only COMPLETED transactions in last 24 hours.
    """
    result = defaultdict(lambda: defaultdict(int))

    for txn in transactions:
        # Filter: only COMPLETED
        if txn.status != Status.COMPLETED:
            continue

        # Filter: only last 24 hours
        hour_diff = get_hour_diff(current_time, txn.startTime)
        if hour_diff < 0 or hour_diff >= 24:
            continue

        # Aggregate: sum by merchantId and hourDiff
        result[txn.merchantId][hour_diff] += txn.amount

    return dict(result)


if __name__ == "__main__":
    current_time = 10  # e.g., 10:00

    transactions = [
        Transaction(100, "merchant_a", Status.COMPLETED, "user1", 8),   # diff=2
        Transaction(200, "merchant_a", Status.COMPLETED, "user2", 5),   # diff=5
        Transaction(150, "merchant_a", Status.COMPLETED, "user3", 8),   # diff=2
        Transaction(300, "merchant_b", Status.COMPLETED, "user1", 7),   # diff=3
        Transaction(50, "merchant_a", Status.PENDING, "user4", 9),      # skip: PENDING
        Transaction(500, "merchant_b", Status.COMPLETED, "user2", -20), # skip: >24h ago
    ]

    result = summarize_transactions(transactions, current_time)
    print(result)
    # {
    #   'merchant_a': {2: 250, 5: 200},  # hour 2: 100+150, hour 5: 200
    #   'merchant_b': {3: 300}
    # }

    for merchant, hourly in sorted(result.items()):
        print(f"{merchant}:")
        for hour_diff, total in sorted(hourly.items()):
            print(f"  {hour_diff}h ago: ${total}")
