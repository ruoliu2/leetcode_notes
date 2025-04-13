import random
from typing import List, Dict
from bisect import bisect_left

TRAITS_KEY = "traits"
N_KEY = "n"
NAME_KEY = "name"


class Solution:
    def __init__(self, config: dict):
        self.traits = {}
        self.max_gen = float("inf")
        self.weights = {}
        for key in config[TRAITS_KEY]:
            self.traits[key] = config[TRAITS_KEY][key]
            denom = sum([weight for _, weight in self.traits[key]])
            w = [weight / denom for _, weight in self.traits[key]]
            for i in range(1, len(w)):
                w[i] += w[i - 1]
            self.weights[key] = w
            self.max_gen = min(self.max_gen, len(self.traits[key]))
        self.n = config[N_KEY]
        self.name = config[NAME_KEY]

    def generateNFT(self, n: int) -> list[dict]:
        res: list[dict] = []

        while len(res) < n:
            nfs: Dict[str, str] = {}
            for key in self.traits:
                nfs[key] = random.choice(self.traits[key])
            res.append(nfs)
        return res

    def generateNFT_dedup(self, n: int) -> list[dict]:
        res: list[dict] = []

        # generate nft until we have n unique ones
        if n > self.max_gen:
            raise ValueError(f"cannot gen {n} number of NFTs")
        while len(res) < n:
            nfs: Dict[str, str] = {}
            for key in self.traits:
                nfs[key] = random.choice(self.traits[key])
                self.traits[key].remove(nfs[key])
            res.append(nfs)

        return res

    def generateNFT_weighted(self) -> dict:
        """
        Generate a single NFT using the weighted random selection for each trait.
        """
        nft: Dict[str, str] = {}
        for key in self.traits:
            choices = [trait for trait, _ in self.traits[key]]
            weights = [weight for _, weight in self.traits[key]]
            # nft[key] = random.choices(choices, weights=weights, k=1)[0]
            N = random.uniform(0, 1)
            idx = bisect_left(self.weights[key], N)
            nft[key] = choices[idx]
        return nft
