import pytest

from models import Card, Rank, Suit
import models
import poker


def test_flush_over_flush():
    cards_by_player_index = {
        0: [Card(Rank.King, Suit.Hearts), Card(Rank.Eight, Suit.Hearts)],
        1: [Card(Rank.Ace, Suit.Hearts), Card(Rank.Seven, Suit.Hearts)]
    } 
    
    board = [
        Card(Rank.Two, Suit.Hearts), 
        Card(Rank.Three, Suit.Hearts), 
        Card(Rank.Four, Suit.Hearts), 
        Card(Rank.Six, Suit.Hearts), 
        Card(Rank.Nine, Suit.Hearts)
        ]

    winning_player_index, winning_hand = poker.determine_winner(cards_by_player_index, board)

    assert winning_player_index == 1
    assert type(winning_hand) == models.Flush
    assert winning_hand.suit == Suit.Hearts
