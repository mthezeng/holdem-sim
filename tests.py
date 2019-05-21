import unittest
from hands import *

class TestHands(unittest.TestCase):
    def test_compare1(self):
        royal = StraightFlush(1)
        t = ThreeOfAKind(5, [Card(1, Suit.HEARTS), Card(10, Suit.HEARTS)])
        self.assertTrue(t < royal)
        self.assertFalse(royal < t)
        self.assertFalse(t > royal)
        self.assertTrue(royal > t)
        self.assertFalse(t == royal)

    def test_compare2(self):
        straight = Straight(10)
        f = FourOfAKind(5, 1)
        self.assertTrue(straight < f)
        self.assertFalse(f < straight)
        self.assertFalse(straight > f)
        self.assertTrue(f > straight)
        self.assertFalse(f == straight)

if __name__ == '__main__':
    unittest.main()
