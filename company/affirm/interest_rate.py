"""
Interest Rate Calculation (Affirm)

Given a loan, calculate the annualized interest rate.

Input:
  - loan_amount: principal in cents (e.g., 6700 = $67.00)
  - total_interest_amount: interest in cents (e.g., 450 = $4.50)
  - loan_start_date: format MM/DD/YY
  - loan_end_date: format MM/DD/YY

Output: annual interest rate as decimal (e.g., 0.12 = 12%)

Formula: rate = (interest / principal) * (365 / days)

Notes:
  - Ignore leap years (Feb = 28 days always)
  - Days = end_date - start_date
"""

DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def compute_interest_rate(
    loan_amount: int, total_interest: int, start_date: str, end_date: str
) -> float:
    def parse_date(s: str) -> tuple[int, int, int]:
        mm, dd, yy = map(int, s.split("/"))
        return (2000 + yy, mm, dd)

    def days_since_epoch(y: int, m: int, d: int) -> int:
        return (y - 2000) * 365 + sum(DAYS_IN_MONTH[: m - 1]) + d

    y1, m1, d1 = parse_date(start_date)
    y2, m2, d2 = parse_date(end_date)
    num_days = days_since_epoch(y2, m2, d2) - days_since_epoch(y1, m1, d1)

    if num_days <= 0 or loan_amount <= 0:
        return 0.0

    return (total_interest / loan_amount) * (365 / num_days)


if __name__ == "__main__":
    # $100 loan, $12 interest, 122 days (Mar 5 - Jul 5)
    rate = compute_interest_rate(10000, 1200, "03/05/22", "07/05/22")
    print(f"Interest rate: {rate:.4f}")  # ~0.36 (36% annual)

    # $67 loan, $4.50 interest, 30 days
    rate2 = compute_interest_rate(6700, 450, "01/01/22", "01/31/22")
    print(f"Interest rate: {rate2:.4f}")  # ~0.82 (82% annual)
