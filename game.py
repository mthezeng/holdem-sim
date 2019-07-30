"""game.py

This file contains core structures relevant to the game of Texas hold'em.
"""

from numpy import random
from hands import *

class Deck:
    """Represents an ordinary, 52-card playing deck."""
    def __init__(self):
        """Constructor for the Deck class, just calls reset."""
        self.cards = []
        self.reset()

    def reset(self):
        """Returns the deck to its original 52 card state."""
        self.cards.clear()
        for s in Suit:
            for i in range(1, 14):
                self.cards.append(Card(i, s))

    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)

    def deal(self, player):
        """Deal a player the top card from this deck."""
        player.addCard(self.cards.pop(0))


class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)
        assert len(self.cards) < 2

    def get_hole_cards(self):
        return self.cards

    def print_hole_cards(self):
        print(self.cards)

    def __str__(self):
        return self.name


class Game:
    def __init__(self, num_players):
        self.players = [Player(i) for i in range(num_players)]
        self.board = []
        self.deck = Deck()

    def show_next_card(self):
        card = self.deck.pop(0)
        self.board.append(card)
        print(card)

    def show_flop(self):
        self.deck.pop(0) # BURN card
        for _ in range(3):
            print('FLOP:')
            self.show_next_card()

    def show_turn(self):
        self.deck.pop(0) # BURN card
        print('TURN:')
        self.show_next_card()

    def show_river(self):
        self.deck.pop(0) # BURN card
        print('RIVER:')
        self.show_next_card()
