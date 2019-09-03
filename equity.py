from random import sample
from itertools import combinations
from time import time

from hands import Card, Suit
from determine_hand import best_hand



def equity_full(hand1, hand2, community_cards=[]):
    assert len(community_cards) >= 3 and len(community_cards) <= 5

    deck = [Card(v, s) for v in range(1, 14) for s in Suit if not Card(v, s) in hand1 + hand2 + community_cards]

    sims = 0
    wins1 = 0
    wins2 = 0
    ties = 0

    r = 5 - len(community_cards)

    for cc in combinations(deck, r): #enumerate the possible combinations of community cards
        sims += 1

        # if sims % 1000 == 0:
            # print(sims, (wins1 + 0.5*ties)/sims)

        b1 = best_hand(list(cc) + hand1 + community_cards)
        b2 = best_hand(list(cc) + hand2 + community_cards)

        if b1 > b2:
            wins1 += 1
        elif b2 > b1:
            wins2 += 1
        else:
            ties += 1

    print(wins1, wins2, ties, sims)
    return (wins1 + 0.5*ties)/sims


def equity_mc(hand1, hand2, total_sims):
    deck = [Card(v, s) for v in range(1, 14) for s in Suit if not Card(v, s) in hand1 + hand2]

    sims = 0
    wins1 = 0
    wins2 = 0
    ties = 0

    while sims < total_sims:
        cc = sample(deck, 5)

        sims += 1
        # if sims % 1000 == 0:
            # print(sims, (wins1 + 0.5*ties)/sims)
        b1 = best_hand(cc + hand1)
        b2 = best_hand(cc + hand2)

        if b1 > b2:
            wins1 += 1
        elif b2 > b1:
            wins2 += 1
        else:
            ties += 1

    print(wins1, wins2, ties, sims)
    return (wins1 + 0.5*ties)/sims


if __name__ == '__main__':
    c1 = input("Player 1, Card 1:\n>> ")
    c2 = input("Player 1, Card 2:\n>> ")
    c3 = input("Player 2, Card 1:\n>> ")
    c4 = input("Player 2, Card 2:\n>> ")

    start = time()

    # print(equity_full([Card(c1), Card(c2)], [Card(c3), Card(c4)]))
    print(equity_mc([Card(c1), Card(c2)], [Card(c3), Card(c4)], 100000))

    end = time()

    print(end - start)
