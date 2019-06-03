from numpy import random
from collections import Counter
from hands import *

class Deck:
    """Represents an ordinary, 52-card playing deck."""
    def __init__(self):
        """Constructor for the Deck class, just calls reset."""
        self.reset()

    def reset(self):
        """Returns the deck to its original 52 card state."""
        self.cards = []
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

    # def determine_hand(self, player):
    #     """Returns a player's best hand given hole cards and community cards."""
    #     cards_available = player.cards + self.board
    def determine_hand(cards_available):
        cards_available.sort(reverse = True)

        # start with high card hand
        hand_type = HighCard(cards_available[:5])

        ## collect information ##
        # count the number of matching cards, store them in most_common
        num_counts = Counter()
        for card in cards_available:
            num_counts[card.get_num()] += 1
        most_common = num_counts.most_common()

        # count number of pairs, trips, and quads
        num_pairs = 0
        num_trips = 0
        num_quads = 0
        for num, count in most_common:
            if count == 4:
                num_quads += 1
            elif count == 3:
                num_trips += 1
            elif count == 2:
                num_pairs += 1

        # count number of cards in each suit
        num_suits = Counter()
        for card in cards_available:
            num_suits[card.get_suit()] += 1

        # check for a straight, storing straight into an array if exists
        # AT98762
        # FIXME: AAT5432 (check for wheel)
        straight_cards = []
        for i in range(len(cards_available) - 5):
            # cur = cards_available[i]
            # next = cards_available[i+1]
            # next_next = cards_available[i+2]
            # if (cur.get_num() == 1 and next.get_num() == 13) or
            #     cur.get_num() - 1 == next.get_num():
            #     straight_cards.append(cur)
            #     if next.get_num() - 1 != next_next.get_num():
            #         straight_cards.append(next)
            # elif len(straight_cards) < 5:
            #     straight_cards = []
            


        ## checks ##


        #check for flushes
        for suit in num_suits:
            if num_suits[suit] >= 5:
                if consecutive_numbers == 5:

                hand_type = Flush([c for c in cards_available if c.get_suit() == suit])
                break

        return hand_type
