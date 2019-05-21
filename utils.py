from numpy import random
from hands import *

class Deck:
    def __init__(self):
        self.reset()

    def reset(self):
        self.cards = []
        for s in Suit:
            for i in range(1, 14):
                self.cards.append(Card(i, s))

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
    #TODO: move to Hand class
    def determine_hand(player):
        cards_available = player.cards + self.board
        cards_available.sort(reverse = True)

        #start with high card hand
        best_hand = cards_available[:5]
        hand_type = HighCard(cards_available[:5])

        #count the number of matching cards
        num_counts = {}
        for card in cards_available:
            if card.get_num() not in num_counts:
                num_counts[card.get_num()] = 1
            else:
                num_counts[card.get_num()] += 1

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
        elif num_pairs == 2:
            hand_type = HandType.TWO_PAIR

        #check for straights
        consecutive_numbers = 0
        for i in range(len(cards_available)):
            if consecutive_numbers == 5:
                hand_type = HandType.STRAIGHT

        #check for flushes
        num_suits = {Suit.HEARTS: 0, Suit.DIAMONDS: 0, Suit.CLUBS: 0, Suit.SPADES: 0}
        for card in cards_available:
            num_suits[card.get_suit()] += 1
        for suit in num_suits:
            if num_suits[suit] >= 5:
                hand_type = HandType.FLUSH
                for card in cards_available:
                    if len(cards_available) < 5 and card.get_suit() == suit:
                        best_hand.append(card)

        return best_hand, hand_type
