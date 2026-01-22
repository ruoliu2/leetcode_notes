"""
Loan Discovery (Affirm)

Parse card event logs to find "suspect" cards. Events format:
  Auth:    "[YYYY-MM-DD HH:MM] CARD #123 AUTH 100"
  Capture: "[YYYY-MM-DD HH:MM] CAPTURE 50"

Find 3 suspect cards:
  1. Most valid (positive) captures in non-active hours (00:00-07:59, 22:00-23:59)
  2. Largest total captured amount (sum of positive captures only)
  3. Most negative capture events

Notes:
  - Keywords (Card, Auth, Capture) are case-insensitive
  - Ignore negative captures in sum calculations
  - Each capture belongs to the most recent auth before it
  - Input NOT guaranteed ordered -> sort by timestamp first
"""

import re
from collections import defaultdict


class LoanDiscovery:
    def __init__(self):
        self.card = None
        self.non_active_count = defaultdict(int)  # card_id -> count
        self.total_positive = defaultdict(int)  # card_id -> sum
        self.negative_count = defaultdict(int)  # card_id -> count

    def _is_non_active(self, hour: int) -> bool:
        return hour <= 7 or hour >= 22

    def _process_event(self, event: str):
        event_lower = event.lower()
        # r"\[\d{4}-\d{2}-\d{2} (\d{2}):\d{2}\]"
        #   \[        - literal open bracket (escaped)
        #   \d{4}     - 4 digits (year)
        #   -         - literal dash
        #   \d{2}     - 2 digits (month)
        #   -         - literal dash
        #   \d{2}     - 2 digits (day)
        #   (space)   - literal space
        #   (\d{2})   - 2 digits (hour) - CAPTURED in group(1)
        #   :         - literal colon
        #   \d{2}     - 2 digits (minute)
        #   \]        - literal close bracket (escaped)
        ts_match = re.search(r"\[\d{4}-\d{2}-\d{2} (\d{2}):\d{2}\]", event)
        if not ts_match:
            return
        hour = int(ts_match.group(1))

        if "auth" in event_lower:
            # r"#(\d+)"
            #   #       - literal hash
            #   (\d+)   - one or more digits (card number) - CAPTURED
            card_match = re.search(r"#(\d+)", event)
            if not card_match:
                return
            self.card = int(card_match.group(1))
        elif "capture" in event_lower and self.card is not None:
            # r"capture\s+(-?\d+)"
            #   capture - literal string "capture"
            #   \s+     - one or more whitespace
            #   (       - start capture group
            #   -?      - optional minus sign
            #   \d+     - one or more digits
            #   )       - end capture group - amount CAPTURED
            amt_match = re.search(r"capture\s+(-?\d+)", event_lower)
            if not amt_match:
                return
            amount = int(amt_match.group(1))
            if amount > 0:
                self.total_positive[self.card] += amount
                if self._is_non_active(hour):
                    self.non_active_count[self.card] += 1
            else:
                self.negative_count[self.card] += 1

    def parse_events(self, events: list[str]):
        def get_ts(e):
            m = re.search(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\]", e)
            return m.group(1) if m else ""

        for event in sorted(events, key=get_ts):
            self._process_event(event)

    def find_suspects(self) -> dict:
        all_cards = set(self.total_positive) | set(self.negative_count)

        def max_by(d):
            return max(
                ((c, d[c]) for c in all_cards), key=lambda x: x[1], default=(None, 0)
            )

        return {
            "most_non_active_captures": max_by(self.non_active_count),
            "largest_captured_amount": max_by(self.total_positive),
            "most_negative_captures": max_by(self.negative_count),
        }


if __name__ == "__main__":
    events = [
        "[2020-11-01 23:58] CARD #98 AUTH 100",
        "[2020-11-01 23:59] CAPTURE 50",
        "[2020-11-02 03:00] CAPTURE 30",
        "[2020-11-02 10:00] CAPTURE -20",
        "[2020-11-03 08:00] CARD #99 AUTH 200",
        "[2020-11-03 09:00] CAPTURE 100",
        "[2020-11-03 23:30] CAPTURE 50",
    ]

    ld = LoanDiscovery()
    ld.parse_events(events)
    print("Suspects:", ld.find_suspects())
    # Card 98: 2 non-active (23:59, 03:00), total=80, 1 negative
    # Card 99: 1 non-active (23:30), total=150, 0 negative
