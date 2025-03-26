"""
High-level:
- Two players: user and dealer.
- One deck reshuffled each round.
- Blackjack with a gambling system for the user.

Cards:
- 52 cards: 4 suits (clubs, diamonds, hearts, spades) with 13 cards each.
- Numbered cards: face value; face cards: 10; ace: 1 or 11.

Round:
- Deal 2 cards to each; one dealer card hidden.
- User draws until they bust or stop.
- Dealer draws until reaching target score (default 17).
- Compare scores to determine winner; user wins double bet, or loses bet.
"""

from enum import Enum
from abc import ABC, abstractmethod
import random


class Suit(Enum):
    CLUBS = "clubs"
    DIAMONDS = "diamonds"
    HEARTS = "hearts"
    SPADES = "spades"


class Card:
    def __init__(self, suit, value):
        self._suit = suit
        self._value = value

    def get_suit(self):
        return self._suit

    def get_value(self):
        return self._value

    def print_card(self):
        print(self.get_suit(), self.get_value())


class Hand:
    def __init__(self):
        self._score = 0
        self._cards = []

    def add_card(self, card):
        self._cards.append(card)
        # Ace: choose 11 if it doesn't bust, else 1
        if card.get_value() == 1:
            self._score += 11 if self._score + 11 <= 21 else 1
        else:
            self._score += card.get_value()
        print("Score:", self._score)

    def get_score(self):
        return self._score

    def get_cards(self):
        return self._cards

    def print_hand(self):
        for card in self.get_cards():
            print(card.get_suit(), card.get_value())


class Deck:
    def __init__(self):
        self._cards = []
        for suit in Suit:
            for value in range(1, 14):
                self._cards.append(Card(suit, min(value, 10)))

    def print_deck(self):
        for card in self._cards:
            card.print_card()

    def draw(self):
        return self._cards.pop()

    def shuffle(self):
        # Shuffle deck in-place
        for i in range(len(self._cards)):
            j = random.randint(0, len(self._cards) - 1)
            self._cards[i], self._cards[j] = self._cards[j], self._cards[i]


class Player(ABC):
    def __init__(self, hand):
        self._hand = hand

    def get_hand(self):
        return self._hand

    def clear_hand(self):
        self._hand = Hand()

    def add_card(self, card):
        self._hand.add_card(card)

    @abstractmethod
    def make_move(self):
        pass


class UserPlayer(Player):
    def __init__(self, balance, hand):
        super().__init__(hand)
        self._balance = balance

    def get_balance(self):
        return self._balance

    def place_bet(self, amount):
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        return amount

    def receive_winnings(self, amount):
        self._balance += amount

    def make_move(self):
        if self.get_hand().get_score() > 21:
            return False
        move = input("Draw card? [y/n] ")
        return move.lower() == "y"


class Dealer(Player):
    def __init__(self, hand):
        super().__init__(hand)
        self._target_score = 17

    def update_target_score(self, score):
        self._target_score = score

    def make_move(self):
        return self.get_hand().get_score() < self._target_score


class GameRound:
    def __init__(self, player, dealer, deck):
        self._player = player
        self._dealer = dealer
        self._deck = deck

    def get_bet(self):
        amount = int(input("Enter a bet amount: "))
        return amount

    def deal_initial_cards(self):
        for _ in range(2):
            self._player.add_card(self._deck.draw())
            self._dealer.add_card(self._deck.draw())
        print("Player hand:")
        self._player.get_hand().print_hand()
        dealer_card = self._dealer.get_hand().get_cards()[0]
        print("Dealer's first card:")
        dealer_card.print_card()

    def cleanup_round(self):
        self._player.clear_hand()
        self._dealer.clear_hand()
        print("Player balance:", self._player.get_balance())

    def play(self):
        self._deck.shuffle()

        if self._player.get_balance() <= 0:
            print("Player has no more money.")
            return

        user_bet = self.get_bet()
        self._player.place_bet(user_bet)

        self.deal_initial_cards()

        # User moves
        while self._player.make_move():
            drawn_card = self._deck.draw()
            print("Player draws", drawn_card.get_suit(), drawn_card.get_value())
            self._player.add_card(drawn_card)
            print("Player score:", self._player.get_hand().get_score())

        if self._player.get_hand().get_score() > 21:
            print("Player busts!")
            self.cleanup_round()
            return

        # Dealer moves
        while self._dealer.make_move():
            self._dealer.add_card(self._deck.draw())

        # Compare scores
        player_score = self._player.get_hand().get_score()
        dealer_score = self._dealer.get_hand().get_score()
        if dealer_score > 21 or player_score > dealer_score:
            print("Player wins")
            self._player.receive_winnings(user_bet * 2)
        elif dealer_score > player_score:
            print("Player loses")
        else:
            print("Draw")
            self._player.receive_winnings(user_bet)
        self.cleanup_round()


player = UserPlayer(1000, Hand())
dealer = Dealer(Hand())

while player.get_balance() > 0:
    GameRound(player, dealer, Deck()).play()
