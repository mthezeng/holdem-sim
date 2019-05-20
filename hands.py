from enum import Enum

class Card:
    card_names = {1: 'A', 13: 'K', 12: 'Q', 11: 'J', 10: 'T'}
    full_names = {
    1: "ace",
    2: "deuce",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "jack",
    12: "queen",
    13: "king"
    }

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
        return "{0} of {1}".format(self.full_names[self.num], self.suit.name.lower())

    def __repr__(self):
        if self.num in self.card_names:
            return '{0}{1}'.format(self.card_names[self.num], self.suit.value)
        else:
            return '{0}{1}'.format(self.num, self.suit.value)

    def get_num(self):
        return self.num

    def get_suit(self):
        return self.suit

class Suit(Enum):
    HEARTS = 'h'
    DIAMONDS = 'd'
    CLUBS = 'c'
    SPADES = 's'

class Hand:
    value = 0 # larger values indicate stronger hands

    def __init__(self):
        pass

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(self, other)

class StraightFlush(Hand):
    value = 9 # strongest hand in holdem poker

    def __init__(self, high_card):
        super().__init__(self)
        self.high_card = high_card

    def __lt__(self, other):
        if isinstance(other, StraightFlush):
            return self.high_card < other.high_card
        return super()

    def __gt__(self, other):
        if isinstance(other, StraightFlush):
            return self.high_card > other.high_card
        return super()

    def __eq__(self, other):
        if super():
            return self.high_card == other.high_card
        return False

    def __str__(self):
        return "Straight flush, {0} to {1}".format(self.high_card, self.high_card - 4)

class FourOfAKind(Hand):
    value = 8

    def __init__(self, quad_card):
        self.quad_card = quad_card

    def __str__(self):
        return "Four of a kind, ".format(str(self.quad_card))

class FullHouse(Hand):
    value = 7

    def __init__(self, set, full):
        pass

class Flush(Hand):
    value = 6

class Straight(Hand):
    value = 5

class ThreeOfAKind(Hand):
    value = 4

class TwoPair(Hand):
    value = 3

class OnePair(Hand):
    value = 2

class HighCard(Hand):
    value = 1
