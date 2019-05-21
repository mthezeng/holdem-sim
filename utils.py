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

        #start with high card hand
        hand_type = HighCard(cards_available[:5])

        #count the number of matching cards
        num_counts = Counter()
        for card in cards_available:
            num_counts[card.get_num()] += 1
        most_common = num_counts.most_common()

        #check for pairs, two pairs, threes of a kind, full houses
        #FIXME
        num_pairs = 0
        trips = False
        for num, count in most_common:
            if count == 3:
                trips = True
            elif count == 2:
                num_pairs += 1

        if num_pairs == 1:
            if trips:
                hand_type = FullHouse(most_common[0][0], most_common[1][0])
            else:
                kickers = [c for c in cards_available if c.get_num() != most_common[0][0]]
                hand_type = OnePair(most_common[0][0], kickers)
        elif num_pairs == 2:
            hand_type = TwoPair(most_common[0][0], most_common[1][0], most_common[2][0])

        #check for straights
        consecutive_numbers = 0
        straight_high = 0
        for i in range(1, len(cards_available)):
            if cards_available[i-1] - cards_available[i] == 1:
                if not straight_high:
                    straight_high = cards_available[i-1]
                consecutive_numbers += 1
        if consecutive_numbers == 5:
            hand_type = Straight(straight_high)

        #check for flushes
        num_suits = Counter()
        for card in cards_available:
            num_suits[card.get_suit()] += 1
        for suit in num_suits:
            if num_suits[suit] >= 5:
                if consecutive_numbers == 5:

                hand_type = Flush([c for c in cards_available if c.get_suit() == suit])
                break

        return hand_type
