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

    def get_fullname(self):
        return self.full_names[self.num]

    def full_name(num):
        return Card.full_names[num]

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

    def __init__(self, high_num):
        super().__init__()
        if not isinstance(high_num, int):
            raise TypeError("high_num must be an int, not {0}".format(type(high_num)))
        if not(5 <= high_num <= 13) and high_num != 1:
            raise ValueError("high card for a straight cannot be {0}".format(high_num))
        self.high_num = high_num

    def __lt__(self, other):
        if isinstance(other, StraightFlush):
            return self.high_num < other.high_num
        return super()

    def __gt__(self, other):
        if isinstance(other, StraightFlush):
            return self.high_num > other.high_num
        return super()

    def __eq__(self, other):
        if super():
            return self.high_num == other.high_num
        return False

    def __ne__(self, other):
        return not self.__eq__(self, other)

    def __str__(self):
        if self.high_num == 1:
            return "Royal flush"
        return "Straight flush, {0} to {1}".format(
        Card.full_name(self.high_num),
        Card.full_name((self.high_num - 4) % 13)
        )

class FourOfAKind(Hand):
    value = 8

    def __init__(self, quad_num, kicker):
        if not isinstance(quad_num, int):
            raise TypeError("quad_num must be an int, not {0}".format(type(quad_num)))
        self.quad_num = quad_num
        self.kicker = kicker

    def __str__(self):
        return "Four of a kind, {0}s".format(Card.full_name(self.quad_num))

class FullHouse(Hand):
    value = 7

    def __init__(self, set, full):
        if not(isinstance(set, int)) or not(isinstance(full, int)):
            raise TypeError("set and full must be ints")
        self.set = set
        self.full = full

    def __lt__(self, other):
        if isinstance(other, FullHouse):
            if self.set == other.set:
                return self.full < other.full
            return self.set < other.set
        return super()

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        if isinstance(other, FullHouse):
            return (self.set == other.set) and (self.full == other.full)
        return super()

    def __ne__(self, other):
        return not self.__eq__(self, other)

    def __str__(self):
        return "Full house, {0}s full of {1}s".format(
        Card.full_name(self.set),
        Card.full_name(self.full)
        )

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
