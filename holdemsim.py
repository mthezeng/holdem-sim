from numpy import random
from enum import Enum

class Card:
    card_names = {1: 'A', 13: 'K', 12: 'Q', 11: 'J', 10: 'T'}

    def __init__(self, number, suit):
        if not isinstance(number, int):
            raise TypeError('number must be an integer')
        if not(1 <= number <= 13):
            raise ValueError('number must be between 1 and 13, inclusive')
        if not isinstance(number, int):
            raise TypeError('suit must be a string')
        self.num = number
        self.suit = suit

    def __str__(self):
        if self.num in card_names:
            return '{0}{1}'.format(card_names[self.num], self.suit.value)
        else:
            return '{0}{1}'.format(self.num, self.suit.value)

class Suit(Enum):
    HEARTS = 'h'
    DIAMONDS = 'd'
    CLUBS = 'c'
    SPADES = 's'

class HandType(Enum):
    STRAIGHT_FLUSH = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    FLUSH = 4
    STRAIGHT = 5
    THREE_OF_A_KIND = 6
    TWO_PAIR = 7
    ONE_PAIR = 8
    HIGH_CARD = 9

class Hand:
    def __init__(self, cards, hand_type):
        if len(cards) != 5:
            raise ValueError("a poker hand must be 5 cards")
        if not isinstance(handtype, HandType):
            raise TypeError("hand_type must be a HandType enum")
        self.cards = cards
        self.hand_type = hand_type
        self.kicker = None # only set by set_kickers if needed

    """Sets kickers. Returns True if there is one, False if there is not."""
    def set_kickers(self, other):
        self_kickers = [card.num for card in self.cards]
        self_kickers.sort(reverse=True)
        other_kickers = [card.num for card in other.cards]
        other_kickers.sort(reverse=True)
        i = 0
        while i < 5 and self_kickers[i] == other_kickers[i]:
            i += 1
        if i == 5:
            return False
        else:
            self.kicker = self_kickers[i]
            other.kicker = other_kickers[i]
            return True

    def __lt__(self, other):
        if self.hand_type != other.hand_type:
            return self.hand_type.value < other.hand_type.value
        else:
            # check kickers
            if not set_kickers(self, other):
                return False
            return self.kicker < other.kicker

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        if self.hand_type != other.hand_type:
            return False
        else:
            return not set_kickers(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

class Deck:
    def __init__(self):
        reset(self)

    def reset(self):
        self.cards = []
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        for j in range(len(suits)):
            for i in range(1, 14):
                self.cards.append(Card(i, j))

    def shuffle(self):
        random.shuffle(self.cards)

    """Deal a player the top card from this deck"""
    def deal(self, player):
        player.addCard(self.cards.pop(0))

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def addCard(self, card):
        self.cards.append(card)
        assert len(self.cards) < 2

    def printHand(self):
        for i in range(len(self.cards)):
            print(self.cards(i))

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

    """Static method that returns a player's best hand
    given hole cards and community cards"""
    def determine_hand(player):
        best_hand = []
        hand_type = HandType.HIGH_CARD
        cards_available = player.cards + self.board
        cards_available.sort(key=lambda card: card.num, reverse = True)

        #start with high card hand
        best_hand = cards_available[:5]

        #count the number of matching cards
        num_counts = {}
        for card in cards_available:
            if card.num not in num_counts:
                num_counts[card.num] = 1
            else:
                num_counts[card.num] += 1

        #check for pairs, two pairs, threes of a kind, full houses
        #FIXME
        num_pairs = 0
        set = False
        for num, count in num_counts:
            if count == 2:
                num_pairs += 1
            elif count == 3:
                set = True

        if num_pairs == 1:
            if set:
                hand_type = HandType.FULL_HOUSE
            else:
                hand_type = HandType.ONE_PAIR
        else if num_pairs == 2:
            hand_type = HandType.TWO_PAIR

        #check for straights
        consecutive_numbers = 0
        for i in range(len(cards_available)):
            if consecutive_numbers == 5:
                hand_type = HandType.STRAIGHT

        #check for flushes
        num_suits = {Suit.HEARTS: 0, Suit.DIAMONDS: 0, Suit.CLUBS: 0, Suit.SPADES: 0}
        for card in cards_available:
            num_suits[card.suit] += 1
        for suit in num_suits:
            if num_suits[suit] >= 5:
                hand_type = HandType.FLUSH
                for card in cards_available:
                    if len(cards_available) < 5 and card.suit == suit:
                        best_hand.append(card)

        return best_hand, hand_type
