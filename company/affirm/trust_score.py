"""
Trust Score (Affirm)

Part 1: Given 2 log files (one per day), format: "date,user_id,order_type,amount"
        Return users who appear on BOTH days AND have >= 2 unique order_types.

Part 2: Calculate trust score for new purchase (user_id, order_type, amount):
        - Order type seen before: +50, else 0
        - Amount in [min, max] range: +50
        - Amount outside range: 50 - (10 * each 10% over), min 0

Follow-up (Streaming): process_line() handles incremental updates - works as-is.

Follow-up (Distributed):
  - Partition by user_id (hash or range) -> each worker owns subset of users
  - Each worker maintains local state: user_types, user_range, user_days
  - No cross-partition joins needed (all user data on same node)
  - For Part 1 query: each worker returns qualified users, merge results
  - For Part 2 query: route to correct partition by user_id, compute locally
  - Scalability: add more partitions as user count grows
"""

from collections import defaultdict


class LogAnalyzer:
    def __init__(self):
        self.user_types = defaultdict(set)  # user_id -> set of order_types
        self.user_range = {}  # user_id -> (min_amt, max_amt)
        self.user_days = defaultdict(set)  # user_id -> set of dates

    def parse_file(self, filepath: str):
        """Parse log file: each line is 'date,user_id,order_type,amount'"""
        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                date, user_id, order_type, amount = line.split(",")
                self._process(date, int(user_id), order_type, float(amount))

    def process_line(self, line: str):
        """For streaming: process single log line"""
        date, user_id, order_type, amount = line.strip().split(",")
        self._process(date, int(user_id), order_type, float(amount))

    def _process(self, date: str, user_id: int, order_type: str, amount: float):
        self.user_days[user_id].add(date)
        self.user_types[user_id].add(order_type)
        if user_id not in self.user_range:
            self.user_range[user_id] = (amount, amount)
        else:
            lo, hi = self.user_range[user_id]
            self.user_range[user_id] = (min(lo, amount), max(hi, amount))

    # Part 1
    def get_qualified_users(self) -> list[int]:
        return [
            uid
            for uid in self.user_days
            if len(self.user_days[uid]) >= 2 and len(self.user_types[uid]) >= 2
        ]

    # Part 2
    def trust_score(self, user_id: int, order_type: str, amount: float) -> int:
        score = 50 if order_type in self.user_types.get(user_id, set()) else 0

        if user_id not in self.user_range:
            return score

        lo, hi = self.user_range[user_id]
        if lo <= amount <= hi:
            return score + 50

        # Outside range: penalty = 10 pts per 10% over
        diff = lo - amount if amount < lo else amount - hi
        base = lo if amount < lo else hi
        if base == 0:
            return score
        pct_over = (diff / base) * 100
        penalty = int(pct_over // 10) * 10
        return score + max(0, 50 - penalty)


if __name__ == "__main__":
    analyzer = LogAnalyzer()

    # File-based usage:
    # analyzer.parse_file("day1.log")
    # analyzer.parse_file("day2.log")

    # Inline test (simulating file content):
    day1 = [
        "2024-01-01,1,phone,100",
        "2024-01-01,1,web,200",
        "2024-01-01,2,phone,150",
        "2024-01-01,3,app,300",
    ]
    day2 = ["2024-01-02,1,app,150", "2024-01-02,2,phone,200", "2024-01-02,4,web,100"]
    for line in day1 + day2:
        analyzer.process_line(line)

    print("Part 1 - Qualified:", analyzer.get_qualified_users())  # [1]

    print("Part 2 - Trust scores:")
    print(analyzer.trust_score(1, "phone", 150))  # 100 (seen + in range)
    print(analyzer.trust_score(1, "phone", 250))  # 75  (seen + 25% over max)
    print(analyzer.trust_score(1, "mail", 150))  # 50  (unseen + in range)
    print(analyzer.trust_score(5, "phone", 100))  # 0   (new user)
