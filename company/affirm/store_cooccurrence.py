"""
Store Co-occurrence (Affirm)

Given shopping records (list of stores per session), find co-occurrence patterns.
For each store, return associated stores sorted by:
  1. Frequency (descending)
  2. Lexicographical (ascending) for ties

Example: [["Amazon", "Walmart", "Costco"], ["Amazon", "Costco", "BestBuy"], ...]
  "Amazon": ["BestBuy", "Costco", "Walmart"]  # BestBuy,Costco: 2x, Walmart: 1x

Similar to letter_pairs.py but with specific output format.
"""
from collections import defaultdict


def store_recommendations(records: list[list[str]]) -> list[list[str]]:
    # Track all unique stores
    all_stores = set()
    # Count co-occurrences: cooccur[store1][store2] = count
    cooccur = defaultdict(lambda: defaultdict(int))

    for record in records:
        stores = set(record)
        all_stores.update(stores)
        for s1 in stores:
            for s2 in stores:
                if s1 != s2:
                    cooccur[s1][s2] += 1

    # Build result: for each store (sorted), get associated stores (sorted by freq desc, then name)
    result = []
    for store in sorted(all_stores):
        associated = cooccur[store]
        # Sort by (-freq, name) -> freq desc, name asc
        sorted_stores = sorted(associated.keys(), key=lambda s: (-associated[s], s))
        result.append(sorted_stores)

    return result


if __name__ == "__main__":
    # Example 1
    records1 = [
        ["Amazon", "Walmart", "Costco"],
        ["Amazon", "Costco", "BestBuy"],
        ["Amazon", "BestBuy"],
        ["HomeDepot", "BestBuy"],
    ]
    print(store_recommendations(records1))
    # [['BestBuy', 'Costco', 'Walmart'],  # Amazon
    #  ['Amazon', 'Costco', 'HomeDepot'],  # BestBuy
    #  ['Amazon', 'BestBuy', 'Walmart'],   # Costco
    #  ['BestBuy'],                        # HomeDepot
    #  ['Amazon', 'Costco']]               # Walmart

    # Example 2
    records2 = [["Amazon"], ["Amazon"], ["Amazon"]]
    print(store_recommendations(records2))  # [[]]

    # Example 3
    records3 = [
        ["Amazon", "Walmart", "Costco", "BestBuy"],
        ["Amazon", "Walmart", "Costco", "BestBuy"],
        ["Amazon", "Walmart", "Costco", "BestBuy"],
    ]
    print(store_recommendations(records3))
    # [['BestBuy', 'Costco', 'Walmart'],  # Amazon (all 3x)
    #  ['Amazon', 'Costco', 'Walmart'],   # BestBuy
    #  ['Amazon', 'BestBuy', 'Walmart'],  # Costco
    #  ['Amazon', 'BestBuy', 'Costco']]   # Walmart
