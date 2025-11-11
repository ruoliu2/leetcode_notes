"""
###### Card Range Obfuscation

**Problem Description**

Payment card numbers consist of 8-19 digits, with the first 6 digits referred to as the Bank Identification Number (BIN).

For a given BIN, all 16-digit card numbers starting with that BIN are considered to be in the BIN range. For example, the BIN 424242 corresponds to card numbers from 4242420000000000 (inclusive) through 4242429999999999 (inclusive).

Stripe's card metadata API may return partial coverage of this BIN range, by providing a list of intervals mapping to card brands (e.g., VISA, MASTERCARD). However, these intervals may have gaps (at the beginning, middle, or end of the BIN range), which can be exploited by fraudsters to probe for valid cards.

Your task is to fill in missing intervals so that the returned intervals fully cover the entire BIN range, with no gaps, and return them in sorted order.

**Input Format**

1. Line 1: A 6-digit BIN.
2. Line 2: A positive integer n, the number of intervals.
3. Next n lines: Each line represents one interval in the format:

start,end,brand

where:

- start and end are 10-digit numbers representing the offset within the BIN range (inclusive).

- brand is an alphanumeric string representing the card brand.

**Output Format**

Return a list of sorted, gap-free intervals, each covering a contiguous portion of the BIN range, formatted as:

start,end,brand

Where start and end are now full 16-digit card numbers (BIN + 10-digit offset). The output intervals must be sorted by start.

**Example**

Input

```
777777
2
1000000000,3999999999,VISA
4000000000,5999999999,MASTERCARD
```

Output

```
7777770000000000,7777773999999999,VISA
7777774000000000,7777775999999999,MASTERCARD
```

**Notes**

- If the input intervals already cover the full BIN range, just return them sorted.
- If there are gaps, fill them with intervals extending from previous/next coverage so that no range is uncovered.
- Be careful with inclusive endpoints — ensure full coverage from BIN0000000000 to BIN9999999999.


"""

from dataclasses import dataclass
from typing import List, Tuple

OFFSET_MIN = 0
OFFSET_MAX = 9_999_999_999  # inclusive
OFFSET_WIDTH = 10  # 10-digit offsets
BIN_WIDTH = 6      # 6-digit BIN
CARD_WIDTH = 16    # 16-digit card numbers

@dataclass
class Interval:
    start: int  # offset within BIN range (inclusive)
    end: int    # offset within BIN range (inclusive)
    brand: str

    def clamp(self) -> "Interval":
        s = max(self.start, OFFSET_MIN)
        e = min(self.end, OFFSET_MAX)
        return Interval(s, e, self.brand)

    def is_valid(self) -> bool:
        return self.start <= self.end and self.end >= OFFSET_MIN and self.start <= OFFSET_MAX


def _merge_and_deoverlap(sorted_intervals: List[Interval]) -> List[Interval]:
    """
    Precondition: intervals are sorted by start.
    - Clamp to legal range.
    - Remove empties.
    - If later interval overlaps earlier, shift its start to previous.end+1.
    - Merge adjacent same-brand intervals.
    """
    out: List[Interval] = []
    for iv in sorted_intervals:
        iv = iv.clamp()
        if not iv.is_valid():
            continue
        if not out:
            out.append(iv)
            continue

        prev = out[-1]

        # If overlapping or touching
        if iv.start <= prev.end:
            # Shift the new interval to start after prev
            shifted_start = prev.end + 1
            if shifted_start > iv.end:
                # Fully covered—drop
                continue
            iv = Interval(shifted_start, iv.end, iv.brand)

        # If adjacent and same brand, merge
        if iv.start == prev.end + 1 and iv.brand == prev.brand:
            out[-1] = Interval(prev.start, iv.end, prev.brand)
        else:
            out.append(iv)

    return out


def _fill_gaps_by_extension(intervals: List[Interval]) -> List[Interval]:
    """
    Extend first interval to OFFSET_MIN if needed, extend gaps by pushing previous.end forward,
    and extend final interval to OFFSET_MAX.
    """
    if not intervals:
        return intervals

    # Extend beginning
    first = intervals[0]
    if first.start > OFFSET_MIN:
        intervals[0] = Interval(OFFSET_MIN, first.end, first.brand)

    # Fill internal gaps by extending the previous interval forward
    for i in range(len(intervals) - 1):
        cur = intervals[i]
        nxt = intervals[i + 1]
        if nxt.start > cur.end + 1:
            # Extend cur forward to bridge the gap
            intervals[i] = Interval(cur.start, nxt.start - 1, cur.brand)

    # Extend end
    last = intervals[-1]
    if last.end < OFFSET_MAX:
        intervals[-1] = Interval(last.start, OFFSET_MAX, last.brand)

    return intervals


def _to_full_card(bin6: str, offset: int) -> str:
    # BIN is 6 digits, offset is 10 digits; combined = 16-digit number
    # We compute as integer to avoid string concat pitfalls, then format to 16 digits.
    # But also validate the bin.
    if len(bin6) != BIN_WIDTH or not bin6.isdigit():
        raise ValueError("BIN must be exactly 6 digits.")
    if offset < OFFSET_MIN or offset > OFFSET_MAX:
        raise ValueError("Offset out of range.")
    full_int = int(bin6) * (10 ** OFFSET_WIDTH) + offset
    return f"{full_int:0{CARD_WIDTH}d}"


def obfuscate_card_ranges(bin6: str, raw_intervals: List[Tuple[int, int, str]]) -> List[Tuple[str, str, str]]:
    """
    Core function: given BIN (6-digit string) and a list of (start, end, brand) offsets,
    return full-card-number intervals that cover the entire BIN range without gaps.
    """
    if not raw_intervals:
        raise ValueError("At least one interval is required to extend coverage.")

    # Sort by start asc, break ties by earlier end asc to stabilize
    intervals = sorted((Interval(s, e, b) for (s, e, b) in raw_intervals), key=lambda x: (x.start, x.end))

    # Normalize overlaps / adjacency
    intervals = _merge_and_deoverlap(intervals)

    if not intervals:
        raise ValueError("No usable intervals remain after normalization.")

    # Fill gaps to cover full range
    intervals = _fill_gaps_by_extension(intervals)

    # Convert to full 16-digit card numbers
    result: List[Tuple[str, str, str]] = []
    for iv in intervals:
        start_full = _to_full_card(bin6, iv.start)
        end_full = _to_full_card(bin6, iv.end)
        result.append((start_full, end_full, iv.brand))
    return result


def parse_input_lines(lines: List[str]) -> Tuple[str, List[Tuple[int, int, str]]]:
    """
    Utility to parse the problem's input format (not strictly needed for pytest, but handy):
      line 1: BIN
      line 2: n
      next n lines: start,end,brand  (offsets are 10-digit decimal, inclusive)
    """
    if len(lines) < 2:
        raise ValueError("Insufficient input lines.")
    bin6 = lines[0].strip()
    n = int(lines[1].strip())
    if len(lines) != 2 + n:
        raise ValueError("Line count does not match n.")
    intervals: List[Tuple[int, int, str]] = []
    for i in range(n):
        s = lines[2 + i].strip()
        parts = s.split(",")
        if len(parts) != 3:
            raise ValueError(f"Bad interval line: {s}")
        start = int(parts[0])
        end = int(parts[1])
        brand = parts[2].strip()
        intervals.append((start, end, brand))
    return bin6, intervals


def format_output(intervals: List[Tuple[str, str, str]]) -> List[str]:
    """
    Convert results to the specified output-line format: start,end,brand
    """
    return [f"{s},{e},{b}" for (s, e, b) in intervals]
