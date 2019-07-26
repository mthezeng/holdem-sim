"""hands.py

This file contains a number of structures representing objects relevant to playing cards and poker hands.
"""

from enum import Enum
from abc import ABC, abstractmethod


class Card:
    """
    This class represents a Card object.

    This class allows for comparisions between the value of playing cards,
    printing various long and short names for each card, and provides several
    static utility methods for dealing with playing cards in general.

    Attributes:
        number (int): The number on the card, e.g. the King of hearts is 13.
        suit (Suit): The suit of the card.
        card_names (dict): Provides short names for some card numbers.
        full_names (dict): Provides long names for all card numbers.
    """
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
        """Constructor for the Card class."""
        if not isinstance(number, int):
            raise TypeError('number must be an integer')
        if not(1 <= number <= 13):
            raise ValueError('number must be between 1 and 13, inclusive')
        if not isinstance(suit, Suit):
            raise TypeError('suit must be a string')
        self.num = number
        self.suit = suit

    def __lt__(self, other):
        """
        Enables the less-than operation for comparing cards. For example,

        >>> ace_of_hearts = Card(1, Suit.HEARTS)
        >>> queen_of_diamonds = Card(12, Suit.DIAMONDS)
        >>> queen_of_diamonds < ace_of_hearts
        True
        """
        if self.get_num() == 1:
            return False
        elif other.get_num() == 1:
            return True
        return self.get_num() < other.get_num()

    def __gt__(self, other):
        """Enables the greater-than operation for comparing the value of cards."""
        return other.__lt__(self)

    def __eq__(self, other):
        """Enables the equality operation for comparing the value of cards."""
        return self.get_num() == other.get_num()

    def __ne__(self, other):
        """Enables the non-equality operation for comparing the value of cards."""
        return not self.__eq__(other)

    def __str__(self):
        """Returns the long name of a card, e.g. king of hearts."""
        return '{0} of {1}'.format(self.full_names[self.num], self.suit.name.lower())

    def __repr__(self):
        """Returns the short name of a card, e.g. Kh."""
        if self.num in self.card_names:
            return '{0}{1}'.format(self.card_names[self.num], self.suit.value)
        else:
            return '{0}{1}'.format(self.num, self.suit.value)

    def is_same(self, other):
        """Returns whether the current card is the exact same card (num and suit) as another."""
        return self.num == other.num and self.suit == other.suit

    def get_num(self):
        """Getter method for the number of the current card instance."""
        return self.num

    def get_suit(self):
        """Getter method for the suit of the current card instance."""
        return self.suit

    def get_fullname(self):
        """Getter method for the full name of the current card instance."""
        return self.full_names[self.num]

    @staticmethod
    def full_name(num):
        """Returns the full name given any card number."""
        return Card.full_names[num]

    @staticmethod
    def lt(num1, num2):
        """Compares two numbers where aces are the highest."""
        assert 1 <= num1 <= 13 and 1 <= num2 <= 13
        if num1 == 1:
            return False
        if num2 == 1:
            return True
        else:
            return num1 < num2


class Suit(Enum):
    """Enumeration representing the four suits that cards may take."""
    HEARTS = 'h'
    DIAMONDS = 'd'
    CLUBS = 'c'
    SPADES = 's'


class Hand(ABC):
    """
    Abstract class representing five-card poker hands.

    Attributes:
        value (int): The strength of the hand. Larger values mean stronger hands.
    """
    value = 0

    @abstractmethod
    def __lt__(self, other):
        """Enables the less-than operation for comparing the value of hands."""
        return self.value < other.value

    @abstractmethod
    def __gt__(self, other):
        """Enables the greater-than operation for comparing the value of hands."""
        return self.value > other.value

    @abstractmethod
    def __eq__(self, other):
        """Enables the equality operation for comparing the value of hands."""
        return self.value == other.value

    @abstractmethod
    def __ne__(self, other):
        """Enables the non-equality operation for comparing the value of hands."""
        return not self.__eq__(other)

    @abstractmethod
    def __str__(self):
        pass


class Straight(Hand):
    """
    Represents a straight in poker.

    A straight is any five-card hand where all the numbers are consecutive.
    For example, 6789T would be a straight. An Ace may complete a straight at
    both the high end and low end: TJQKA and A2345 are both valid straights.
    However, beyond that, straights cannot wrap around: QKA23 is not a straight.

    Attributes:
        high_num (int): The highest card of the straight.
        value (int): The strength of the hand. Larger values mean stronger hands.
    """
    value = 5

    def __init__(self, high_num):
        if not isinstance(high_num, int):
            raise TypeError('high_num must be an int, not {0}'.format(type(high_num)))
        if not(5 <= high_num <= 13) and high_num != 1:
            raise ValueError('high card for a straight cannot be {0}'.format(high_num))
        self.high_num = high_num

    def __lt__(self, other):
        if type(self) == type(other):
            # type(self) and type(other) are used because StraightFlush inherits this method
            return Card.lt(self.high_num, other.high_num)
        return self.value < other.value

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        if type(self) == type(other):
            return self.high_num == other.high_num
        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'Straight, {0} to {1}'.format(
            Card.full_name(self.high_num),
            Card.full_name((self.high_num - 4) % 13)
        )


class StraightFlush(Straight):
    """
    Represents a straight flush in poker.

    This class represents a straight flush in poker, which is five cards of
    consecutive numbers, all the same suit. This class inherits the methods
    of the Straight class, since the algorithm for comparing two straight
    flushes is the same as that for comparing two straights. A straight flush
    is the highest value hand in Texas hold'em poker.

    Attributes:
        high_num (int): The highest card of the straight.
        value (int): The strength of the hand. Larger values mean stronger hands.
    """
    value = 9

    def __str__(self):
        if self.high_num == 1:
            return 'Royal flush'
        return 'Straight flush, {0} to {1}'.format(
            Card.full_name(self.high_num),
            Card.full_name((self.high_num - 4) % 13)
        )


class TwoKindsHand(Hand):
    """
    Abstract class that represents a five-card hand that only has two kinds of cards.

    FourOfAKind and FullHouse have very similar representations, since both
    hands only feature two kinds of cards. This class combines both of their
    implementations. TwoKindsHand should itself never be instantiated, only
    FourOfAKind and FullHouse.

    Attributes:
        big (int): The number that is repeated more frequently in the hand.
        small (int): The number that is repeated less frequently in the hand.
    """
    def __init__(self, big, small):
        """Constructor for TwoKindsHand."""
        if not(isinstance(big, int) and isinstance(small, int)):
            raise TypeError('arguments must be ints')
        if not(1 <= big <= 13 and 1 <= small <= 13):
            raise ValueError('invalid card nums')
        if big == small:
            raise ValueError('invalid card nums for {0}'.format(type(self)))
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
        return not self.__eq__(other)


class FourOfAKind(TwoKindsHand):
    """
    Represents a four of a kind, inheriting the methods of TwoKindsHand.

    A four of a kind has all four cards of the same number, plus one extra called
    the kicker. For example, four queens plus a king would be four of a kind
    with a king kicker. In Texas hold'em, a kicker might come into play if
    there are three or four of the same kind card within the community cards,
    allowing two or more players in the hand to hold four of a kind.

    Attributes:
        big (int): The number that is repeated four times in the hand.
        small (int): The kicker.
        value (int): The strength of the hand. Larger values mean stronger hands.
    """
    value = 8

    def __str__(self):
        return 'Four of a kind, {0}s'.format(Card.full_name(self.big))


class FullHouse(TwoKindsHand):
    """
    Represents a full house, inheriting the methods of TwoKindsHand.

    A full house has three cards with the same number, plus two other cards also
    sharing the same number. For example, three queens plus two kings would be
    a full house, queens full of kings.

    Attributes:
        big (int): The number that is repeated three times in the hand.
        small (int): The number that is repeated two times in the hand.
        value (int): The strength of the hand. Larger values mean stronger hands.
    """
    value = 7

    def __str__(self):
        return 'Full house, {0}s full of {1}s'.format(
            Card.full_name(self.big),
            Card.full_name(self.small)
        )


class NoRepeats(Hand):
    """
    Abstract class representing a hand with no repeating numbers, excluding straights.

    This is an abstract superclass for flushes and high cards, since both hands
    do not contain any repeating cards and therefore require a list of all five
    cards in the hand to be passed into the constructor. Comparisons between
    two flushes and two high cards require traversing the whole list in the
    worst case, comparing each respective card in each hand.

    Attributes:
        cards (list): A reverse-sorted list of all five cards in the hand.
        high_card (Card): The card of the highest value within the hand.
    """
    def __init__(self, cards):
        self.cards = cards
        self.cards.sort(reverse=True)
        self.high_card = self.cards[0]

    def __lt__(self, other):
        if type(self) == type(other):
            for i in range(len(self.cards)):
                if self.cards[i] != other.cards[i]:
                    return Card.lt(self.cards[i], other.cards[i])
            return False
        return self.value < other.value

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        if type(self) == type(other):
            return self.cards == other.cards
        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)


class Flush(NoRepeats):
    """
    Represents a flush in poker.

    A flush is a poker hand where all five cards have the same suit. Comparing
    this hand with other flushes requires the same method as comparing two high
    card hands, so both flushes and high cards inherit the same superclass
    comparison methods in NoRepeats.

    Attributes:
        cards (list): A list of Card instances comprising the five-card hand.
        value (int): The strength of the hand. Larger values mean stronger hands.
    """
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
        super().__init__(cards)

    def __str__(self):
        return 'Flush, {0} high'.format(self.high_card.get_fullname())


class ThreeOfAKind(Hand):
    """
    Represents a three of a kind in poker.

    A three of a kind has three cards with the same number, plus two extras
    called kickers. For example, three aces plus a king and a queen would be
    three of a kind, aces.

    Attributes:
        num (int): The number repeated three times in the hand.
        kickers (list): A reverse-sorted list of the two kickers (Cards) in the hand.
        value (int): The strength of the hand. Larger values mean stronger hands.
    """
    value = 4

    def __init__(self, num, kickers):
        if not isinstance(num, int):
            raise TypeError('num should be an int')
        if not isinstance(kickers, list):
            raise TypeError('kickers should be a list of two cards')
        if len(kickers) != 2:
            raise ValueError('kickers should be 2 cards, not {0}'.format(len(kickers)))
        for c in kickers:
            if not isinstance(c, Card):
                # We are using the Card class so that we get ace-high logic when sorting.
                raise TypeError('kickers should be Cards, not {0}'.format(type(c)))
            if c.get_num() == num:
                raise ValueError('kicker cannot be same num as the set')
        self.num = num
        self.kickers = kickers
        self.kickers.sort(reverse=True)

    def __lt__(self, other):
        if isinstance(other, ThreeOfAKind):
            if self.num != other.num:
                return Card.lt(self.num, other.num)
            for i in range(len(self.kickers)):
                if self.kickers[i] != other.kickers[i]:
                    return Card.lt(self.kickers[i], other.kickers[i])
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
        return 'Three of a kind, {0}s'.format(Card.full_name(self.num))


class TwoPair(Hand):
    """
    Represents a two pair in poker.

    A two pair is a hand consisting of two pairs, plus one extra card called
    the kicker. A pair is any two cards with the same number. For example,
    two aces, two kings, and a queen would be two pair, aces and queens.

    Attributes:
        big (int): The larger of the two pairs, e.g. 1 in AAKKQ.
        small (int): The smaller of the two pairs, e.g. 13 in AAKKQ.
        kicker (int): The kicker, e.g. 12 in AAKKQ.
        value (int): The strength of the hand. Larger values mean stronger hands.
    """
    value = 3

    def __init__(self, big, small, kicker):
        if not(isinstance(big, int) and isinstance(small, int) and isinstance(kicker, int)):
            raise TypeError('All parameters must be ints')
        if not(1 <= big <= 13 and 1 <= small <= 13 and 1 <= kicker <= 13):
            raise ValueError('invalid card nums')
        if big == small or big == kicker or small == kicker:
            raise ValueError('not a two pair')
        self.big = big
        self.small = small
        if self.small > self.big:
            self.big, self.small = self.small, self.big
        self.kicker = kicker

    def __lt__(self, other):
        if isinstance(other, TwoPair):
            if self.big != other.big:
                return Card.lt(self.big, other.big)
            elif self.small != other.small:
                return Card.lt(self.small, other.small)
            else:
                return Card.lt(self.kicker, other.kicker)
        return self.value < other.value

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        if isinstance(other, TwoPair):
            return self.big == other.big and self.small == other.small and self.kicker == other.kicker
        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'Two pair, {0}s and {1}s'.format(
            Card.full_name(self.big),
            Card.full_name(self.small)
        )


class OnePair(Hand):
    """
    Represents a one pair hand in poker.

    A one pair hand contains a pair of cards with the same number, plus three
    extra cards with different numbers called kickers. If two players have the
    same pair, the value of their hand is compared by the value of the kickers.

    Attributes:
        pair_num (int): The number that is paired in the hand.
        kickers (list): A reverse-sorted list of the kickers in the hand.
        value (int): The strength of the hand. Larger values mean stronger hands.
    """
    value = 2

    def __init__(self, pair_num, kickers):
        if not isinstance(pair_num, int):
            raise TypeError('pair_num must be an int')
        if not isinstance(kickers, list):
            raise TypeError('kickers must be a list')
        if len(kickers) != 3:
            raise ValueError('kickers must have length 3')
        for c in kickers:
            if not isinstance(c, Card):
                raise TypeError('kickers must be a list of Cards')
            if c.get_num() == pair_num:
                raise ValueError('kickers cannot be the same as the pair_num')
        self.pair_num = pair_num
        self.kickers = kickers
        self.kickers.sort(reverse=True)

    def __lt__(self, other):
        if isinstance(other, OnePair):
            if other.pair_num != self.pair_num:
                return self.pair_num < self.pair_num
            else:
                return self.kickers < other.kickers
        return self.value < other.value

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        if isinstance(other, OnePair):
            return self.pair_num == other.pair_num and self.kickers == other.kickers
        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'One pair, {0}s'.format(Card.full_name(self.pair_num))


class HighCard(NoRepeats):
    """
    Represents a high card hand in poker.

    When a hand contains no straights, flushes, or repeated cards, its value is
    determined by value of the highest card in the hand. Comparing this hand
    with other high card hands requires the same method as comparing two
    flushes, so both flushes and high cards inherit the same superclass
    comparison methods in NoRepeats.

    Attributes:
        cards (list): A list of Card instances comprising the five-card hand.
        value (int): The strength of the hand. Larger values mean stronger hands.
    """
    value = 1

    def __init__(self, cards):
        if not isinstance(cards, list):
            raise TypeError('the list of cards must be passed in')
        if len(cards) != 5:
            raise ValueError('the list of cards must have five cards')
        for c in cards:
            if not isinstance(c, Card):
                raise TypeError('{0} in cards is not a Card'.format(c))
        super().__init__(cards)

    def __str__(self):
        return '{0} high'.format(Card.full_name(self.high_card))
