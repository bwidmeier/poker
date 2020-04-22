import enum

import models


class Suit(enum.Enum):
    Clubs = 'c'
    Diamonds = 'd'
    Hearts = 'h'
    Spades = 's'


class Rank(enum.Enum):
    Two = enum.auto()
    Three = enum.auto()
    Four = enum.auto()
    Five = enum.auto()
    Six = enum.auto()
    Seven = enum.auto()
    Eight = enum.auto()
    Nine = enum.auto()
    Ten = enum.auto()
    Jack = enum.auto()
    Queen = enum.auto()
    King = enum.auto()
    Ace = enum.auto()


class Card():
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f'[{self.rank}, {self.suit}]'

    def __repr__(self):
        return self.__str__()

    def __gt__(self, other):
        return self.rank.value > other.rank.value


class Hand():
    def __init__(self, cards, hand_rank):
        self.cards = cards
        self.hand_rank = hand_rank

    def __gt__(self, other):
        if self.hand_rank > other.hand_rank:
            return True

        return self.cards > other.cards


class StraightFlush(Hand):
    def __init__(self, cards, suit, high_card):
        super().__init__(cards, 9)
        self.suit = suit
        self.high_card = high_card


class FourOfAKind(Hand):
    def __init__(self, cards, rank, kicker):
        super().__init__(cards, 8)
        self.rank = rank
        self.kicker = kicker


class FullHouse(Hand):
    def __init__(self, cards, threesome_rank, twosome_rank):
        super().__init__(cards, 7)
        self.threesome_rank = threesome_rank
        self.twosome_rank = twosome_rank


class Flush(Hand):
    def __init__(self, cards, suit):
        super().__init__(cards, 6)
        self.suit = suit


class Straight(Hand):
    def __init__(self, cards, high_rank):
        super().__init__(cards, 5)
        self.high_rank = high_rank


class ThreeOfAKind(Hand):
    def __init__(self, cards, threesome_rank, kicker1, kicker2):
        super().__init__(cards, 4)
        self.threesome_rank = threesome_rank
        self.kicker1 = kicker1
        self.kicker2 = kicker2


class TwoPair(Hand):
    def __init__(self, cards, twosome1_rank, twosome2_rank, kicker):
        super().__init__(cards, 3)
        self.twosome1_rank = twosome1_rank
        self.twosome2_rank = twosome2_rank
        self.kicker = kicker


class Pair(Hand):
    def __init__(self, cards, twosome_rank, kicker1, kicker2, kicker3):
        super().__init__(cards, 2)
        self.twosome_rank = twosome_rank
        self.kicker1 = kicker1
        self.kicker2 = kicker2
        self.kicker3 = kicker3


class HighCard(Hand):
    def __init__(self, cards):
        super().__init__(cards, 1)
