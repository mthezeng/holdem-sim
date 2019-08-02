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
        """Removes and returns the top card of the deck."""
        return self.cards.pop(0)


class Player:
    def __init__(self, name, seat_num):
        self.name = name
        self.seat = seat_num
        self.cards = []
        self.stack = 0
        self.sitting_out = False
        self.comments = ""

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

    def get_comments(self):
        return self.comments

    def set_comments(self, comment):
        """Comments about player to print in show_game_state, usually bets."""
        self.comments = comment

    def get_stack(self):
        return self.stack

    def change_stack(self, delta):
        self.stack += delta

    def set_stack(self, amount):
        self.stack = amount

    def sit_out(self):
        self.sitting_out = True

    def come_back(self):
        self.sitting_out = False

    def __str__(self):
        return self.name


class Game:
    def __init__(self, num_players, small_blind, big_blind):
        self.num_players = num_players
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.players = [Player(input("Seat {0} name: ".format(i)), i) for i in range(1, num_players + 1)]
        self.board = []
        self.deck = Deck()
        self.deck.shuffle()
        self.actions = []
        self.button = self.determine_button(self.players)
        self.pot = 0.0
        # TODO: self.players_in_hand

    def get_player_at_seat(self, seat_num):
        """Returns Player at the specified seat number."""
        return self.players[seat_num - 1]

    def take_turns(self):
        """Generator which starts from the small blind and rotates clockwise."""
        button_seat = self.button.get_seat_num()
        cur_seat = (button_seat + 1) % self.num_players
        while True:
            # print(cur_seat)
            yield self.get_player_at_seat(cur_seat)
            cur_seat = (cur_seat + 1) % self.num_players

    def show_game_state(self, show_cards=True):
        print('-----\nCurrent game state:')
        print('Pot: ${0}'.format(self.pot))
        for p in self.players:
            if p is self.button:
                button = "[BTN] "
            else:
                button = ""
            if show_cards:
                hole_cards = p.get_hole_cards()
            else:
                hole_cards = ""
            print("  Seat {0} ({1}) {2}{3} {4}".format(
                p.get_seat_num(), p.get_name(), button, hole_cards, p.get_comments()))

    def start_game(self):
        for p in self.players:
            p.set_stack(100 * self.big_blind)
        self.deal_hole_cards()
        self.show_game_state()
        self.post_blinds()
        self.show_game_state()

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

    def move_button(self):
        """Moves button one seat to the left."""
        self.button = self.get_player_at_seat((self.button.get_seat_num() + 1) % self.num_players)

    def deal_hole_cards(self):
        turn_gen = self.take_turns()
        cur_player = next(turn_gen)
        while len(cur_player.get_hole_cards()) < 2:
            print("Card dealt to {0}.".format(cur_player))
            self.deck.deal(cur_player)
            cur_player = next(turn_gen)

    def post_blinds(self):
        turns = self.take_turns()
        small = next(turns)
        self.bet(small, self.small_blind)
        small.set_comments("posts SB: {0}".format(self.small_blind))
        big = next(turns)
        self.bet(big, self.big_blind)
        big.set_comments("posts BB: {0}".format(self.big_blind))

    def round_of_betting(self):
        # TODO: get bet sizing from all players
        bet_prior = False
        for p in self.take_turns():
            if bet_prior:
                action = input("Fold/Call/Raise?: ")
            else:
                action = input("Fold/Check/Bet?: ")
            if action == "Bet" or action == "bet":
                bet_size = int(input("What is p's bet?: "))
                self.bet(p, bet_size)
                p.set_comments("bets: {0}")
                self.show_game_state()

    def bet(self, player, amount):
        player.change_stack(-amount)
        self.pot += amount

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
        self.player = player


