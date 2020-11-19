import pytest

from tcp_ip_poker import Card, Deck, Suit

def test_cards():
    deck = Deck()
    suit_cards = {}
    for suit in Suit:
        suit_cards[suit] = []

    assert len(deck) == Deck.MAX_DECK_SIZE
    while card := deck.get_card():
        suit_cards[card.suit].append(card)
    assert len(deck) == 0

    for suit in suit_cards:
        assert len(suit_cards[suit]) == 13  
    
