import unittest
from hands import *
from utils import Game.determine_hand

class ComparisonTests(unittest.TestCase):
    def test_compare_diff1(self):
        higher = StraightFlush(1)
        lower = ThreeOfAKind(5, [Card(1, Suit.HEARTS), Card(10, Suit.HEARTS)])
        self.assertTrue(lower < higher)
        self.assertFalse(higher < lower)
        self.assertFalse(lower > higher)
        self.assertTrue(higher > lower)
        self.assertFalse(lower == higher)
        self.assertFalse(higher == lower)

    def test_compare_diff2(self):
        higher = FourOfAKind(5, 1)
        lower = Straight(10)
        self.assertTrue(lower < higher)
        self.assertFalse(higher < lower)
        self.assertFalse(lower > higher)
        self.assertTrue(higher > lower)
        self.assertFalse(lower == higher)
        self.assertFalse(higher == lower)

    def test_compare_diff3(self):
        higher = FullHouse(1, 13)
        lower = Straight(10)
        self.assertTrue(lower < higher)
        self.assertFalse(higher < lower)
        self.assertFalse(lower > higher)
        self.assertTrue(higher > lower)
        self.assertFalse(lower == higher)
        self.assertFalse(higher == lower)


    def test_compare_diff4(self):
        higher = Straight(10)
        lower = TwoPair(1, 2, 13)
        self.assertTrue(lower < higher)
        self.assertFalse(higher < lower)
        self.assertFalse(lower > higher)
        self.assertTrue(higher > lower)
        self.assertFalse(lower == higher)
        self.assertFalse(higher == lower)

    def test_compare_diff5(self):
        higher = StraightFlush(1)
        lower = Straight(1)
        self.assertTrue(lower < higher)
        self.assertFalse(higher < lower)
        self.assertFalse(lower > higher)
        self.assertTrue(higher > lower)
        self.assertFalse(lower == higher)
        self.assertFalse(higher == lower)

    def test_compare_diff6(self):
        higher = FourOfAKind(1, 13)
        lower = FullHouse(1, 13)
        self.assertTrue(lower < higher)
        self.assertFalse(higher < lower)
        self.assertFalse(lower > higher)
        self.assertTrue(higher > lower)
        self.assertFalse(lower == higher)
        self.assertFalse(higher == lower)

    def test_compare_same1(self):
        higher = TwoPair(1, 9, 13)
        lower = TwoPair(2, 9, 13)
        self.assertTrue(lower < higher)
        self.assertFalse(higher < lower)
        self.assertFalse(lower > higher)
        self.assertTrue(higher > lower)
        self.assertFalse(lower == higher)
        self.assertFalse(higher == lower)

    def test_compare_same2(self):
        higher = Straight(1)
        lower = Straight(10)
        self.assertTrue(lower < higher)
        self.assertFalse(higher < lower)
        self.assertFalse(lower > higher)
        self.assertTrue(higher > lower)
        self.assertFalse(lower == higher)
        self.assertFalse(higher == lower)

    def test_compare_same3(self):
        higher = ThreeOfAKind(1, [Card(8, Suit.HEARTS), Card(9, Suit.HEARTS)])
        lower = ThreeOfAKind(10, [Card(12, Suit.HEARTS), Card(11, Suit.HEARTS)])
        self.assertTrue(lower < higher)
        self.assertFalse(higher < lower)
        self.assertFalse(lower > higher)
        self.assertTrue(higher > lower)
        self.assertFalse(lower == higher)
        self.assertFalse(higher == lower)

class DetermineHandTests(unittest.TestCase):
    def test_straight():
        cards_available = [
        Card(1, Suit.CLUBS),
        Card(2, Suit.DIAMONDS),
        Card(3, Suit.DIAMONDS),
        Card(4, Suit.SPADES),
        Card(5, Suit.SPADES),
        Card(10, Suit.HEARTS),
        Card(1, Suit.SPADES)
        ]
        hand = determine_hand(cards_available)
        self.assertTrue(isinstance(hand, Straight))

if __name__ == '__main__':
    unittest.main()
