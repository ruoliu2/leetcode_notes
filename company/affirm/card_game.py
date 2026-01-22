"""
Nun Card Game (Affirm)

Part 1: Two-Player Game
-----------------------
Deck: 52 unique cards [1..52], shuffled and dealt evenly (26 each).
Each turn: both flip top card, higher card wins both (1 point per card).
Continue until no cards left. Higher score wins.
Tiebreaker: player with highest card in their win pile.

Part 2: N-Player Game
---------------------
Input: game(players: list[str], M: int) - N player names, M cards [1..M]
Deal: M // N cards each, leftover cards dealt randomly one-by-one.
Each turn: all players flip, highest card wins all N cards.
Tiebreaker (same score): highest card in win pile.
Output: print winner's name.

Example: game(["Joe", "Jill", "Bob"], 5) - 3 players, 5 cards
"""

import random
from collections import deque


class CardGame:
    def __init__(self, players: list[str], M: int):
        self.players = players
        self.N = len(players)
        self.M = M

        deck = list(range(1, M + 1))
        random.shuffle(deck)

        # Deal cards: M // N each, then leftover randomly
        base = M // self.N
        self.hands = [deque(deck[i * base : (i + 1) * base]) for i in range(self.N)]
        leftover = deck[self.N * base :]
        for i, card in enumerate(leftover):
            self.hands[i % self.N].append(card)

        self.scores = [0] * self.N
        self.max_cards = [0] * self.N

    def draw_card(self) -> list[tuple[int, int]]:
        """Each player with cards flips top card. Returns [(card, player_idx), ...]"""
        flipped = []
        for i in range(self.N):
            if self.hands[i]:
                flipped.append((self.hands[i].popleft(), i))
        return flipped

    def score(self, flipped: list[tuple[int, int]]):
        """Winner takes all flipped cards, update score and max_card."""
        if not flipped:
            return
        winning_card, winner_idx = max(flipped, key=lambda x: x[0])
        self.scores[winner_idx] += len(flipped)
        self.max_cards[winner_idx] = max(self.max_cards[winner_idx], winning_card)

    def has_cards(self) -> bool:
        return any(self.hands)

    def get_winner(self) -> str:
        """Return winner: highest score, tiebreaker = highest card in win pile."""
        results = [
            (self.scores[i], self.max_cards[i], self.players[i]) for i in range(self.N)
        ]
        results.sort(key=lambda x: (x[0], x[1]), reverse=True)
        return results[0][2]

    def play(self) -> str:
        while self.has_cards():
            flipped = self.draw_card()
            self.score(flipped)
        winner = self.get_winner()
        print(winner)
        return winner


def game(players: list[str], M: int) -> str:
    return CardGame(players, M).play()


if __name__ == "__main__":
    print("=== Two Player Game ===")
    game(["Player 1", "Player 2"], 52)

    print("\n=== N-Player Game ===")
    game(["Joe", "Jill", "Bob"], 17)  # 3 players, 17 cards
    game(["A", "B", "C", "D", "E"], 17)  # 5 players, 17 cards (2 get 4, 3 get 3)
