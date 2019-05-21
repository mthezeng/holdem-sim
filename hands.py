from enum import Enum

class Card:
    card_names = {1: 'A', 13: 'K', 12: 'Q', 11: 'J', 10: 'T'}
    full_names = {
    1: 'ace',
    2: 'deuce',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine',
    10: 'ten',
    11: 'jack',
    12: 'queen',
    13: 'king'
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

    def __lt__(self, other):
        if self.get_num() == 1:
            return False
        elif other.get_num() == 1:
            return True
        return self.get_num() < other.get_num()

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        return self.get_num() == other.get_num()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return '{0} of {1}'.format(self.full_names[self.num], self.suit.name.lower())

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
        raise NotImplementedError()

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(self, other)

class Straight(Hand):
    value = 5

    def __init__(self, high_num):
        if not isinstance(high_num, int):
            raise TypeError('high_num must be an int, not {0}'.format(type(high_num)))
        if not(5 <= high_num <= 13) and high_num != 1:
            raise ValueError('high card for a straight cannot be {0}'.format(high_num))
        self.high_num = high_num

    def __lt__(self, other):
        if type(self) == type(other):
            return self.high_num < other.high_num
        return self.value < other.value

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        if type(self) == type(other):
            return self.high_num == other.high_num
        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(self, other)

    def __str__(self):
        return 'Straight, {0} to {1}'.format(
        Card.full_name(self.high_num),
        Card.full_name((self.high_num - 4) % 13)
        )

class StraightFlush(Straight):
    value = 9 # strongest hand in holdem poker

    def __str__(self):
        if self.high_num == 1:
            return 'Royal flush'
        return 'Straight flush, {0} to {1}'.format(
        Card.full_name(self.high_num),
        Card.full_name((self.high_num - 4) % 13)
        )

"""
FourOfAKind and FullHouse have very similar representations
TwoKindsHand should never be instantiated
"""
class TwoKindsHand(Hand):
    """big is the number repeated more frequently than small in the hand"""
    def __init__(self, big, small):
        if isinstance(self, TwoKindsHand):
            raise NotImplementedError('TwoKindsHand is abstract')
        if not(isinstance(big, int)) or not(isinstance(small, int)):
            raise TypeError('arguments must be ints')
        self.big = big
        self.small = small

    def __lt__(self, other):
        if type(self) == type(other):
            if self.big == other.big:
                return self.small < other.small
            return self.big < other.big
        return self.value < other.value

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        if type(self) == type(other):
            return (self.big == other.big) and (self.small == other.small)
        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(self, other)

class FourOfAKind(TwoKindsHand):
    value = 8

    def __init__(self, big, small):
        super()

    def __str__(self):
        return 'Four of a kind, {0}s'.format(Card.full_name(self.quad_num))

class FullHouse(TwoKindsHand):
    value = 7

    def __init__(self, big, small):
        super()

    def __str__(self):
        return 'Full house, {0}s full of {1}s'.format(
        Card.full_name(self.set),
        Card.full_name(self.full)
        )

class Flush(Hand):
    value = 6

    def __init__(self, cards):
        if not isinstance(cards, list):
            raise TypeError('the list of cards must be passed in')
        if len(cards) != 5:
            raise ValueError('the list of cards must have five cards')
        suit = cards[0].get_suit()
        for c in cards:
            if not isinstance(c, Card):
                raise TypeError('{0} in cards is not a Card'.format(c))
            if c.get_suit() != suit:
                raise ValueError('Not a flush: expected {0} but got {1}'.format(suit, c.get_suit()))
        self.cards = cards
        self.cards.sort(reverse = True)

    def __lt__(self, other):
        if isinstance(other, Flush):
            for i in range(len(self.cards)):
                if self.cards[i] != other.cards[i]:
                    return self.cards[i] < other.cards[i]
            return False
        return self.value < other.value

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        if isinstance(other, Flush):
            return self.cards == other.cards
        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'Flush, {0} high'.format(self.cards[0].get_fullname())

class ThreeOfAKind(Hand):
    value = 4

    def __init__(self, set_num, kickers):
        if not isinstance(set_num, int):
            raise TypeError('set_num should be an int')
        if not isinstance(kickers, list):
            raise TypeError('kickers should be a list of two cards')
        if len(kickers) != 2:
            raise ValueError('kickers should be 2 cards, not {0}'.format(len(kickers)))
        for c in kickers:
            if not isinstance(c, Card):
                raise TypeError('kickers should be Cards, not {0}'.format(type(c)))
        self.num = set_num
        self.kickers = kickers
        self.kickers.sort()

    def __lt__(self, other):
        if isinstance(other, ThreeOfAKind):
            if self.num != other.num:
                return self.num < other.num
            for i in range(len(self.kickers)):
                if self.kickers[i] != other.kickers[i]:
                    return self.kickers[i] < other.kickers[i]
            return False
        return self.value < other.value

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        if isinstance(other, ThreeOfAKind):
            return self.num == other.num and self.kickers == other.kickers
        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "Three of a kind, {0}s".format(Card.full_name(self.num))

class TwoPair(Hand):
    value = 3

class OnePair(Hand):
    value = 2

class HighCard(Hand):
    value = 1
