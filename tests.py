"""tests.py

This file contains unit tests responsible for testing the functionality of the functions
in hands.py, determine_hand.py, and game.py.
"""
import unittest
from hands import *
from determine_hand import get_hand


class ComparisonTests(unittest.TestCase):
    """This class contains tests for hands.py."""
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

    def test_compare_diff7(self):
        higher = FourOfAKind(1, 13)
        lower = FourOfAKind(13, 1)
        self.assertTrue(lower < higher)
        self.assertFalse(higher < lower)
        self.assertFalse(lower > higher)
        self.assertTrue(higher > lower)
        self.assertFalse(lower == higher)
        self.assertFalse(higher == lower)

    def test_compare_diff8(self):
        higher = OnePair(1, [Card(5, Suit.CLUBS), Card(7, Suit.CLUBS), Card(10, Suit.CLUBS)])
        lower = OnePair(13, [Card(5, Suit.CLUBS), Card(7, Suit.CLUBS), Card(10, Suit.CLUBS)])
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
    """This class contains tests for determine_hand.py."""

    def test_straight1(self):
        cards_available = [
            Card(5, Suit.CLUBS),
            Card(6, Suit.DIAMONDS),
            Card(7, Suit.DIAMONDS),
            Card(8, Suit.SPADES),
            Card(9, Suit.SPADES)
        ]
        hand = get_hand(cards_available)
        self.assertTrue(isinstance(hand, Straight))
        self.assertEqual(9, hand.high_num)

    def test_straight2(self):
        # wheel (ace-to-five) straight
        cards_available = [
            Card(1, Suit.CLUBS),
            Card(5, Suit.HEARTS),
            Card(3, Suit.DIAMONDS),
            Card(4, Suit.SPADES),
            Card(2, Suit.SPADES)
        ]
        hand = get_hand(cards_available)
        self.assertTrue(isinstance(hand, Straight))
        self.assertEqual(5, hand.high_num)

    def test_straight3(self):
        # nut (ten-to-ace) straight
        cards_available = [
            Card(1, Suit.HEARTS),
            Card(11, Suit.SPADES),
            Card(13, Suit.DIAMONDS),
            Card(10, Suit.HEARTS),
            Card(12, Suit.DIAMONDS)
        ]
        hand = get_hand(cards_available)
        self.assertTrue(isinstance(hand, Straight))
        self.assertEqual(1, hand.high_num)

    def test_flush(self):
        cards_available = [
            Card(1, Suit.CLUBS),
            Card(4, Suit.CLUBS),
            Card(7, Suit.CLUBS),
            Card(2, Suit.CLUBS),
            Card(11, Suit.CLUBS)
        ]
        hand = get_hand(cards_available)
        self.assertTrue(isinstance(hand, Flush))
        self.assertEqual(1, hand.high_card.get_num())

    def test_straight_flush1(self):
        # nut (ten-to-ace) straight flush, a.k.a. royal flush
        cards_available = [
            Card(1, Suit.HEARTS),
            Card(11, Suit.HEARTS),
            Card(13, Suit.HEARTS),
            Card(10, Suit.HEARTS),
            Card(12, Suit.HEARTS)
        ]
        hand = get_hand(cards_available)
        self.assertTrue(isinstance(hand, StraightFlush))
        self.assertEqual(1, hand.high_num)

    def test_straight_flush2(self):
        # wheel (ace-to-five) straight flush
        cards_available = [
            Card(1, Suit.DIAMONDS),
            Card(5, Suit.DIAMONDS),
            Card(3, Suit.DIAMONDS),
            Card(4, Suit.DIAMONDS),
            Card(2, Suit.DIAMONDS)
        ]
        hand = get_hand(cards_available)
        self.assertTrue(isinstance(hand, StraightFlush))
        self.assertEqual(5, hand.high_num)

    def test_straight_flush3(self):
        cards_available = [
            Card(5, Suit.CLUBS),
            Card(6, Suit.CLUBS),
            Card(7, Suit.CLUBS),
            Card(8, Suit.CLUBS),
            Card(9, Suit.CLUBS)
        ]
        hand = get_hand(cards_available)
        self.assertTrue(isinstance(hand, StraightFlush))
        self.assertEqual(9, hand.high_num)

    def test_quads1(self):
        cards_available = [
            Card(1, Suit.CLUBS),
            Card(1, Suit.DIAMONDS),
            Card(1, Suit.SPADES),
            Card(1, Suit.HEARTS),
            Card(13, Suit.CLUBS)
        ]
        hand = get_hand(cards_available)
        self.assertTrue(isinstance(hand, FourOfAKind))
        self.assertEqual(1, hand.big)
        self.assertEqual(13, hand.small)

    def test_quads2(self):
        cards_available = [
            Card(2, Suit.CLUBS),
            Card(2, Suit.DIAMONDS),
            Card(2, Suit.SPADES),
            Card(2, Suit.HEARTS),
            Card(1, Suit.CLUBS)
        ]
        hand = get_hand(cards_available)
        self.assertTrue(isinstance(hand, FourOfAKind))
        self.assertEqual(2, hand.big)
        self.assertEqual(1, hand.small)

    def test_fullhouse1(self):
        cards_available = [
            Card(1, Suit.CLUBS),
            Card(1, Suit.DIAMONDS),
            Card(1, Suit.SPADES),
            Card(13, Suit.HEARTS),
            Card(13, Suit.CLUBS)
        ]
        hand = get_hand(cards_available)
        self.assertTrue(isinstance(hand, FullHouse))
        self.assertEqual(1, hand.big)
        self.assertEqual(13, hand.small)

    def test_fullhouse2(self):
        cards_available = [
            Card(2, Suit.CLUBS),
            Card(2, Suit.DIAMONDS),
            Card(2, Suit.SPADES),
            Card(1, Suit.HEARTS),
            Card(1, Suit.CLUBS)
        ]
        hand = get_hand(cards_available)
        self.assertTrue(isinstance(hand, FullHouse))
        self.assertEqual(2, hand.big)
        self.assertEqual(1, hand.small)

    def test_invalidhand1(self):
        # five of a kind and duplicated card
        cards_available = [
            Card(2, Suit.CLUBS),
            Card(2, Suit.DIAMONDS),
            Card(2, Suit.SPADES),
            Card(2, Suit.HEARTS),
            Card(2, Suit.CLUBS)
        ]
        with self.assertRaises(ValueError):
            get_hand(cards_available)

    def test_invalidhand2(self):
        # two of clubs is repeated twice
        cards_available = [
            Card(2, Suit.CLUBS),
            Card(2, Suit.DIAMONDS),
            Card(2, Suit.CLUBS),
            Card(1, Suit.HEARTS),
            Card(1, Suit.CLUBS)
        ]
        with self.assertRaises(ValueError):
            get_hand(cards_available)

    def test_invalidhand3(self):
        # wheel (ace-to-five) straight flush
        cards_available = [
            Card(1, Suit.DIAMONDS),
            Card(5, Suit.DIAMONDS),
            Card(3, Suit.DIAMONDS),
            Card(5, Suit.DIAMONDS),
            Card(2, Suit.DIAMONDS)
        ]
        with self.assertRaises(ValueError):
            get_hand(cards_available)

    def test_trips1(self):
        cards_available = [
            Card(1, Suit.CLUBS),
            Card(1, Suit.HEARTS),
            Card(1, Suit.DIAMONDS),
            Card(10, Suit.DIAMONDS),
            Card(13, Suit.DIAMONDS)
        ]
        hand = get_hand(cards_available)
        self.assertTrue(isinstance(hand, ThreeOfAKind))
        self.assertEqual(1, hand.num)
        self.assertEqual(2, len(hand.kickers))
        self.assertEqual(13, hand.kickers[0].get_num())
        self.assertEqual(10, hand.kickers[1].get_num())

    def test_trips2(self):
        cards_available = [
            Card(10, Suit.CLUBS),
            Card(10, Suit.HEARTS),
            Card(10, Suit.DIAMONDS),
            Card(13, Suit.DIAMONDS),
            Card(7, Suit.DIAMONDS)
        ]
        hand = get_hand(cards_available)
        self.assertTrue(isinstance(hand, ThreeOfAKind))
        self.assertEqual(10, hand.num)
        self.assertEqual(2, len(hand.kickers))
        self.assertEqual(13, hand.kickers[0].get_num())
        self.assertEqual(7, hand.kickers[1].get_num())

    def test_twopair1(self):
        cards_available = [
            Card(10, Suit.CLUBS),
            Card(13, Suit.HEARTS),
            Card(7, Suit.DIAMONDS),
            Card(13, Suit.DIAMONDS),
            Card(7, Suit.CLUBS)
        ]
        hand = get_hand(cards_available)
        self.assertTrue(isinstance(hand, TwoPair))
        self.assertEqual(13, hand.big)
        self.assertEqual(7, hand.small)
        self.assertEqual(10, hand.kicker)

    def test_twopair2(self):
        cards_available = [
            Card(1, Suit.CLUBS),
            Card(13, Suit.HEARTS),
            Card(7, Suit.DIAMONDS),
            Card(1, Suit.DIAMONDS),
            Card(7, Suit.CLUBS)
        ]
        hand = get_hand(cards_available)
        self.assertTrue(isinstance(hand, TwoPair))
        self.assertEqual(1, hand.big)
        self.assertEqual(7, hand.small)
        self.assertEqual(13, hand.kicker)

    def test_onepair1(self):
        cards_available = [
            Card(1, Suit.CLUBS),
            Card(13, Suit.HEARTS),
            Card(10, Suit.DIAMONDS),
            Card(1, Suit.DIAMONDS),
            Card(7, Suit.CLUBS)
        ]
        hand = get_hand(cards_available)
        self.assertTrue(isinstance(hand, OnePair))
        self.assertEqual(1, hand.pair_num)

    def test_onepair2(self):
        cards_available = [
            Card(10, Suit.CLUBS),
            Card(13, Suit.HEARTS),
            Card(10, Suit.DIAMONDS),
            Card(1, Suit.DIAMONDS),
            Card(7, Suit.CLUBS)
        ]
        hand = get_hand(cards_available)
        self.assertTrue(isinstance(hand, OnePair))
        self.assertEqual(10, hand.pair_num)

    def test_highcard(self):
        cards_available = [
            Card(10, Suit.CLUBS),
            Card(13, Suit.HEARTS),
            Card(9, Suit.DIAMONDS),
            Card(1, Suit.DIAMONDS),
            Card(7, Suit.CLUBS)
        ]
        hand = get_hand(cards_available)
        self.assertTrue(isinstance(hand, HighCard))
        self.assertEqual(1, hand.high_card.get_num())
        self.assertEqual(13, hand.cards[1].get_num())


if __name__ == '__main__':
    unittest.main()
