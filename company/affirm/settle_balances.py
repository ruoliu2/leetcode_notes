"""
Settle Balances (Affirm)

Background: Affirm moves money between customers, merchants, and third parties.

Part 1: Given transactions [sender, receiver, amount] and starting balances,
        return end-of-day balances after all transactions.

Part 2: Given unsettled balances (some positive, some negative),
        return minimum transactions to settle all balances to 0.
        Greedy: match largest debtor with largest creditor.

Example:
  Input:  {0: -100, 1: 150, 2: -200, 3: 150}
          (0 owes 100, 1 is owed 150, 2 owes 200, 3 is owed 150)
  Output: [[2, 1, 150], [2, 3, 50], [0, 3, 100]]
          {0: 0, 1: 0, 2: 0, 3: 0}
"""

import heapq


def get_balance_dict(
    transactions: list[list[int]], balances: dict[int, int]
) -> dict[int, int]:
    """Part 1: Process transactions, return final balances."""
    for sender, receiver, amount in transactions:
        balances[sender] -= amount
        balances[receiver] += amount
    return balances


def settle_balances(
    balances: dict[int, int],
) -> tuple[list[list[int]], dict[int, int]]:
    """
    Part 2 (Optimal): Backtracking, LC 465 style. O(n!) with pruning.
    """
    # Filter non-zero balances: (id, amount)
    items = [(k, v) for k, v in balances.items() if v != 0]
    best = [float("inf"), []]  # [min_count, best_transactions]

    def bt(i, txns):
        # Skip already settled (balance == 0)
        while i < len(items) and items[i][1] == 0:
            i += 1

        # Base: all settled
        if i == len(items):
            if len(txns) < best[0]:
                best[0], best[1] = len(txns), txns[:]
            return

        # Prune: can't beat current best
        if len(txns) >= best[0]:
            return

        ki, vi = items[i]
        # Try settling items[i] with each opposite-sign balance
        for j in range(i + 1, len(items)):
            kj, vj = items[j]
            if vi * vj < 0:  # opposite signs can settle
                amt = min(abs(vi), abs(vj))
                # Direction: debtor pays creditor
                txn = [ki, kj, amt] if vi < 0 else [kj, ki, amt]
                # Update balances (vi<0: vi+=amt, vj-=amt, else opposite)
                items[i] = (ki, vi + amt if vi < 0 else vi - amt)
                items[j] = (kj, vj - amt if vi < 0 else vj + amt)
                bt(i, txns + [txn])
                # Restore for next iteration
                items[i], items[j] = (ki, vi), (kj, vj)

    bt(0, [])
    return best[1], {k: 0 for k in balances}


if __name__ == "__main__":
    # Part 1 test
    transactions = [[0, 1, 100], [2, 3, 200], [3, 1, 50]]
    start = {0: 0, 1: 0, 2: 0, 3: 0}
    print("Part 1:", get_balance_dict(transactions, start))

    # Part 2 test
    input1 = {0: -100, 1: 150, 2: -200, 3: 150}
    print("Optimal:", settle_balances(input1))

    input2 = {0: -800, 1: -500, 2: -100, 3: -100, 4: 100, 5: 100, 6: 1300}
    print("Optimal:", settle_balances(input2))

    input3 = {0: -5, 1: -5, 2: 3, 3: 3, 4: 4}
    print("Optimal:", settle_balances(input3))
