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
        if self.num in self.card_names:
            return '{0}{1}'.format(self.card_names[self.num], self.suit.value)
        else:
            return '{0}{1}'.format(self.num, self.suit.value)

    def __repr__(self):
        return self.__str__()

class Suit(Enum):
    HEARTS = 'h'
    DIAMONDS = 'd'
    CLUBS = 'c'
    SPADES = 's'

class Hand:
    value = 0 # larger values indicate stronger hands

    def __init__(self, cards):
        if len(cards) != 5:
            raise ValueError("a poker hand must be 5 cards")
        if not isinstance(handtype, HandType):
            raise TypeError("hand_type must be a HandType enum")
        self.cards = cards

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

    def __init__(self, cards):
        super().__init__(self, cards)
        self.cards.sort(key=lambda card: card.num, reverse = True)
        self.high_card = self.cards[0]

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

class FourOfAKind(Hand):
    value = 8

class FullHouse(Hand):
    value = 7

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
