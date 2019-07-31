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
        player.add_card(self.cards.pop(0))

    def burn_card(self):
        """Discard the top card of the deck."""
        self.cards.pop(0)

    def get_top_card(self):
        """Returns the top card of the deck."""
        return self.cards.pop(0)


class Player:
    def __init__(self, name, seat_num):
        self.name = name
        self.seat = seat_num
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)
        assert len(self.cards) <= 2

    def get_hole_cards(self):
        return self.cards

    def print_hole_cards(self):
        print(self.cards)

    def get_seat_num(self):
        return self.seat

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name


class Game:
    def __init__(self, num_players):
        self.players = [Player(input("Seat {0} name: ".format(i)), i) for i in range(1, num_players + 1)]
        self.board = []
        self.deck = Deck()
        self.deck.shuffle()
        self.actions = []
        self.button = self.determine_button(self.players)

    def start_game(self):
        self.deal_hole_cards()

    def determine_button(self, players):
        """Deals every player one card face-up. Highest value card determines button."""
        print("-----\nDealing for position:")
        exposed_cards = []
        for p in players:
            exposed_cards.append(self.deck.get_top_card())
            print("Seat {0} ({1}) dealt {2}".format(p.get_seat_num(), p.get_name(), exposed_cards[-1]))

        max_so_far = exposed_cards[0].get_num()
        players_with_max = []
        for i in range(len(exposed_cards)):
            cur_num = exposed_cards[i].get_num()
            if Card.lt(max_so_far, cur_num):
                max_so_far = cur_num
                players_with_max.clear()
                players_with_max.append(players[i])
            elif cur_num == max_so_far:
                players_with_max.append(players[i])

        if len(players_with_max) > 1:
            print("A tie was detected. Re-dealing the players who tied:")
            return self.determine_button(players_with_max)
        else:
            self.deck.reset()
            self.deck.shuffle()
            print("Button set to seat {0}".format(players_with_max[0].get_seat_num()))
            return players_with_max[0]

    def deal_hole_cards(self):
        # FIXME: start from left of button
        for _ in range(2):
            for p in self.players:
                print("Card dealt to {0}.".format(p))
                self.deck.deal(p)

    # def round_of_betting(self):
    #     # TODO: get bet sizing from all players
    #     for p in self.players:


    def show_next_card(self):
        """Procedure called by show_flop, show_turn, and show_river that exposes one card from deck."""
        card = self.deck.pop(0)
        self.board.append(card)
        print(card)

    def show_flop(self):
        self.deck.burn_card()
        for _ in range(3):
            print('FLOP:')
            self.show_next_card()

    def show_turn(self):
        self.deck.burn_card()
        print('TURN:')
        self.show_next_card()

    def show_river(self):
        self.deck.burn_card()
        print('RIVER:')
        self.show_next_card()

    def get_players(self):
        return self.players


class Hero:
    """A view of the Game class that focuses on one player's hole cards."""
    def __init__(self, game, player):
        self.game = game

