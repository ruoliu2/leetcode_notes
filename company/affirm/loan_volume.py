"""
Loan Volume Tracker (Affirm / LC 362 variant)

API:
  process_loan(amount, ts) - record loan amount at time
  get_loan_volume(ts) - return total amount in last 1 hour

Solution 1: List + bisect. O(1) put, O(log n + k) get
Solution 2: Circular Array. O(1) put, O(1) get (amortized)
"""
from bisect import bisect_right

HOUR = 3600


class LoanTrackerSimple:
    """
    List + bisect. O(1) put, O(log n) get.
    Core: binary search cutoff index, prefix sum for O(1) range sum.
    """

    def __init__(self):
        self.times = []    # sorted timestamps
        self.prefix = [0]  # prefix[i] = sum of amounts[0:i]

    def process_loan(self, amount: float, ts: int):
        self.times.append(ts)
        self.prefix.append(self.prefix[-1] + amount)

    def get_loan_volume(self, ts: int) -> float:
        # Find first index > (ts - HOUR), sum everything after
        idx = bisect_right(self.times, ts - HOUR)
        return self.prefix[-1] - self.prefix[idx]


class LoanTracker:
    """
    Circular Array. O(1) put, O(1) get (amortized).
    Core: 3600 buckets (1/sec), running total, lazy clear stale buckets.
    """

    def __init__(self):
        self.buckets = [[0, 0] for _ in range(HOUR)]  # [ts, sum] per second
        self.total = 0      # running sum of last hour
        self.last_ts = 0    # last accessed timestamp

    def _clear_stale(self, ts: int):
        # Clear buckets that have become > 1 hour old since last access
        if ts - self.last_ts >= HOUR:
            self.buckets = [[0, 0] for _ in range(HOUR)]
            self.total = 0
        else:
            for t in range(self.last_ts + 1, ts + 1):
                self.total -= self.buckets[t % HOUR][1]  # subtract old
                self.buckets[t % HOUR] = [0, 0]          # reset bucket
        self.last_ts = ts

    def process_loan(self, amount: float, ts: int):
        self._clear_stale(ts)  # lazy clear before write
        idx = ts % HOUR
        if self.buckets[idx][0] != ts:  # new second, reset bucket
            self.buckets[idx] = [ts, 0]
        self.buckets[idx][1] += amount
        self.total += amount

    def get_loan_volume(self, ts: int) -> float:
        self._clear_stale(ts)  # lazy clear before read
        return self.total      # O(1) return running total


if __name__ == "__main__":
    # Test both solutions
    for Tracker in [LoanTrackerSimple, LoanTracker]:
        print(f"=== {Tracker.__name__} ===")
        t = Tracker()
        t.process_loan(100, 0)
        t.process_loan(200, 1)
        t.process_loan(300, 2)
        print(t.get_loan_volume(10))    # 600
        print(t.get_loan_volume(3601))  # 500 (100 expired)
        print(t.get_loan_volume(3602))  # 300 (100,200 expired)
        print(t.get_loan_volume(3603))  # 0 (all expired)
