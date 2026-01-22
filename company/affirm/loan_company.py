"""
Loan Company Hierarchy (Affirm)

Part 1: Given parent->children map, find topmost parent for any company.
        {"DD": ["AA"], "AA": ["BB", "CC"]} -> CC's top parent is DD

Part 2: Match transactions to loans by (user_id, top_parent, amount).
        Loan/Txn format: [id, user_id, company/merchant, amount]
        Return matching loan_id per transaction, or -1.

Edge case: A company may appear only as a parent (no children in map).
"""

from collections import defaultdict


class LoanSystem:
    def __init__(self, company_map: dict[str, list[str]]):
        self.parent = {}
        for p, children in company_map.items():
            for c in children:
                self.parent[c] = p

    def find_top_parent(self, company: str) -> str:
        if company not in self.parent:
            return company
        self.parent[company] = self.find_top_parent(self.parent[company])
        return self.parent[company]

    def match_transactions(
        self,
        loans: list[tuple[int, int, str, int]],
        transactions: list[tuple[int, int, str, int]],
    ) -> list[int]:
        index = defaultdict(list)
        for loan_id, user_id, company, amount in loans:
            key = (user_id, self.find_top_parent(company), amount)
            index[key].append(loan_id)

        res = []
        for _, user_id, merchant, amount in transactions:
            key = (user_id, self.find_top_parent(merchant), amount)
            matched = index.get(key)
            res.append(matched[0] if matched else -1)
        return res


if __name__ == "__main__":
    company_map = {"AA": ["BB", "CC"], "DD": ["AA"]}

    loans = [(1, 100, "CC", 500), (2, 100, "BB", 300), (3, 200, "DD", 1000)]
    transactions = [
        (10, 100, "CC", 500),  # -> 1 (CC->AA->DD matches loan 1's CC->AA->DD)
        (11, 100, "BB", 300),  # -> 2 (BB->AA->DD matches loan 2's BB->AA->DD)
        (12, 200, "AA", 1000),  # -> 3 (AA->DD matches loan 3's DD)
        (13, 100, "CC", 999),  # -> -1 (no match - wrong amount)
    ]

    system = LoanSystem(company_map)
    print(system.match_transactions(loans, transactions))  # [1, 2, 3, -1]
