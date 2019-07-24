from hands import *
from collections import Counter


class DetermineHand:
	"""
	This class contains a number of methods for identifying poker hands given the cards that comprise them.

	Attributes:
		cards (list): A list of five Card instances comprising a poker hand.
	"""

	def __init__(self, cards):
		if not isinstance(cards, list):
			raise TypeError('The list of cards must be passed in.')
		if len(cards) != 5:
			raise ValueError('The list of cards must have five cards.')
		for c in cards:
			if not isinstance(c, Card):
				raise TypeError('{0} in cards is not a Card'.format(c))
		self.cards = cards
		self.cards.sort(reverse=True)

	def identify(self):
		# count the number of matching cards, store them in most_common
		num_counts = Counter()
		for card in self.cards:
			num_counts[card.get_num()] += 1
		most_common = num_counts.most_common()

		# check for each hand type
		if self._is_straight_flush():
			return StraightFlush(self.cards[0].get_num())

		elif self._is_quads():
			return FourOfAKind(most_common[0][0], most_common[1][0])

		elif self._is_full_house():
			return FullHouse(most_common[0][0], most_common[1][0])

		elif self._is_flush():
			return Flush(self.cards)

		elif self._is_straight():
			return Straight(self.cards[0].get_num())

		elif self._is_trips():
			kickers = []
			for c in self.cards:
				if c.get_num() != most_common[0]:
					kickers.append(c)
			return ThreeOfAKind(most_common[0], kickers)

		elif self._is_two_pair():
			paired_cards = []
			kicker = -1
			for e in most_common:
				if e[1] == 2:
					paired_cards.append(e[0])
				if e[1] == 1:
					kicker = e[1]
			assert kicker > 0
			return TwoPair(max(paired_cards), min(paired_cards), kicker)

		else:
			return HighCard(self.cards)

	def _is_straight_flush(self):
		raise NotImplementedError()

	def _is_quads(self):
		raise NotImplementedError()

	def _is_full_house(self):
		raise NotImplementedError()

	def _is_flush(self):
		suit = self.cards[0].get_suit()
		for c in self.cards:
			if c.get_suit() != suit:
				return False
		return True

	def _is_straight(self):
		# FIXME: wheel straight is sorted as A5432
		for i in range(4):
			if self.cards[i] != self.cards[i+1] + 1:
				return False
		return True

	def _is_trips(self):
		raise NotImplementedError()

	def _is_two_pair(self):
		raise NotImplementedError()

	def _is_pair(self):
		raise NotImplementedError()


# TODO: determine best five-card hand given seven cards (flop, turn, river, hole cards)
