"""
Coin Change (Affirm Variant)

Given coins [1,2,5,10] and amount, return ANY valid combination as a map.
Guaranteed solution exists (coin 1 always present).

Approach: Greedy - divide by largest coin first, use remainder for next.

LC Coin Change (Minimum): Need DP, greedy fails for min coins.
"""
from functools import cache
from math import inf


def coin_change_any(coins: list[int], amount: int) -> dict[int, int]:
    """Greedy: return any valid combination."""
    result = {}
    for coin in sorted(coins, reverse=True):
        if amount >= coin:
            result[coin] = amount // coin
            amount %= coin
    return result


def coin_change_min(coins: list[int], amount: int) -> tuple[int, dict[int, int]]:
    """LC 322: DP with memoization, return (min_count, combination)."""
    # dp(i) = (fewest coins, coin used to reach this state)
    @cache
    def dp(i):
        if i == 0:
            return (0, None)
        if i < 0:
            return (inf, None)
        best = (inf, None)
        for coin in coins:
            cnt, _ = dp(i - coin)
            if cnt + 1 < best[0]:
                best = (cnt + 1, coin)
        return best

    count, _ = dp(amount)
    if count == inf:
        return -1, {}

    # Backtrack to get combination
    result = {}
    curr = amount
    while curr > 0:
        _, coin = dp(curr)
        result[coin] = result.get(coin, 0) + 1
        curr -= coin

    return count, result


if __name__ == "__main__":
    coins = [1, 2, 5, 10]

    print("=== Greedy (any solution) ===")
    print(coin_change_any(coins, 100))  # {10: 10}
    print(coin_change_any(coins, 27))   # {10: 2, 5: 1, 2: 1}

    print("\n=== DP (minimum count + combination) ===")
    print(coin_change_min(coins, 100))  # (10, {10: 10})
    print(coin_change_min(coins, 27))   # (4, {10: 2, 5: 1, 2: 1})

    # Case where greedy != minimum
    coins2 = [1, 3, 4]
    print("\n=== Greedy vs DP (coins=[1,3,4], amount=6) ===")
    print("Greedy:", coin_change_any(coins2, 6))  # {4: 1, 1: 2} = 3 coins
    print("DP:    ", coin_change_min(coins2, 6))  # (2, {3: 2})
