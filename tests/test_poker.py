import pytest

from tcp_ip_poker import Card, Deck, Suit
from tcp_ip_poker.poker import VictoryCombination

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

    
def test_victory_combinations():
    high_card_hand = [
        Card(Suit.DIAMONDS, 13),
        Card(Suit.DIAMONDS, 12),
        Card(Suit.SPADES, 7),
        Card(Suit.SPADES, 4),
        Card(Suit.HEARTS, 3)
    ]

    one_pair_hand = [
        Card(Suit.SPADES, 10),
        Card(Suit.HEARTS, 10),
        Card(Suit.SPADES, 7),
        Card(Suit.SPADES, 4),
        Card(Suit.HEARTS, 3)
    ]

    two_pair_hand = [
        Card(Suit.SPADES, 10),
        Card(Suit.HEARTS, 10),
        Card(Suit.SPADES, 8),
        Card(Suit.HEARTS, 8),
        Card(Suit.HEARTS, 3)
    ]

    three_of_kind_hand = [
        Card(Suit.SPADES, 10),
        Card(Suit.HEARTS, 10),
        Card(Suit.DIAMONDS, 10),
        Card(Suit.SPADES, 4),
        Card(Suit.HEARTS, 3)
    ]

    straight_hand = [
        Card(Suit.SPADES, 8),
        Card(Suit.HEARTS, 5),
        Card(Suit.SPADES, 6),
        Card(Suit.SPADES, 7),
        Card(Suit.HEARTS, 9)
    ]

    flush_hand = [
        Card(Suit.SPADES, 10),
        Card(Suit.SPADES, 1),
        Card(Suit.SPADES, 7),
        Card(Suit.SPADES, 4),
        Card(Suit.SPADES, 3)
    ]

    full_house_hand = [
        Card(Suit.SPADES, 10),
        Card(Suit.HEARTS, 10),
        Card(Suit.DIAMONDS, 10),
        Card(Suit.SPADES, 3),
        Card(Suit.HEARTS, 3)
    ]

    four_of_kind_hand = [
        Card(Suit.SPADES, 10),
        Card(Suit.HEARTS, 10),
        Card(Suit.DIAMONDS, 10),
        Card(Suit.CLUBS, 10),
        Card(Suit.HEARTS, 3)
    ]

    straight_flush_hand = [
        Card(Suit.SPADES, 13),
        Card(Suit.SPADES, 12),
        Card(Suit.SPADES, 11),
        Card(Suit.SPADES, 10),
        Card(Suit.SPADES, 9)
    ]

    assert VictoryCombination.determine_best_combination(high_card_hand) == VictoryCombination.HIGH_CARD
    assert VictoryCombination.determine_best_combination(one_pair_hand) == VictoryCombination.PAIR
    assert VictoryCombination.determine_best_combination(two_pair_hand) == VictoryCombination.TWO_PAIRS
    assert VictoryCombination.determine_best_combination(three_of_kind_hand) == VictoryCombination.THREE_OF_A_KIND
    assert VictoryCombination.determine_best_combination(straight_hand) == VictoryCombination.STRAIGHT
    assert VictoryCombination.determine_best_combination(flush_hand) == VictoryCombination.FLUSH
    assert VictoryCombination.determine_best_combination(full_house_hand) == VictoryCombination.FULL_HOUSE
    assert VictoryCombination.determine_best_combination(four_of_kind_hand) == VictoryCombination.FOUR_OF_A_KIND
    assert VictoryCombination.determine_best_combination(straight_flush_hand) == VictoryCombination.STRAIGHT_FLUSH
