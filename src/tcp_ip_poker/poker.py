from __future__ import annotations
from typing import Union, Sequence
import enum, itertools, random

class Suit(enum.Enum):
    """ Value is a tuple of description and unicode symbol """
    SPADES = ('Spades', '♤')
    CLUBS = ('Clubs','♣')
    HEARTS = ('Hearts','♡')
    DIAMONDS = ('Diamonds','♢')

class Card:
    MIN_VALUE = 1
    VALUES = [
        ('Ace', 'A'),
        ('Two', '2'),
        ('Three', '3'),
        ('Four', '4'),
        ('Five', '5'),
        ('Six', '6'),
        ('Seven', '7'),
        ('Eight', '8'),
        ('Nine', '9'),
        ('Ten', '10'),
        ('Jack', 'J'),
        ('Queen', 'Q'),
        ('King', 'K')
    ]


    def __init__(self, suit: Suit, value: int):
        if not self.MIN_VALUE <=  value <= len(self.VALUES) + self.MIN_VALUE:
            raise ValueError('Invalid value')
        if not isinstance(suit, Suit):
            raise ValueError('Invalid suit')
        self._suit = suit
        self._value = value

    def __eq__(self, card: Union[Card, int]) -> bool:
        if isinstance(card, Card):
            card = card.value
        return self.value == card

    def __lt__(self, card: Union[Card, int]) -> bool:
        if isinstance(card, Card):
            card = card.value
        return  self.value < card

    def __gt__(self, card: Union[Card, int]) -> bool:
        if isinstance(card, Card):
            card = card.value
        return  self.value > card

    def __str__(self):
        return f"{self.get_value()} of {self.suit.value[0]} {self.suit.value[1]}"

    # --- Properties ---

    @property
    def value(self) -> int:
        return self._value

    @property
    def suit(self) -> Suit:
        return self._suit


    # --- Public methods ---

    def get_value(self, long = True) -> str:
        """ Returns the cards value as string. If long is true returns full description
        otherwise returns short description.
        """
        return self.VALUES[self.value - self.MIN_VALUE][int(not long)]

    def get_short_string(self) -> str:
        """ Returns the short version from card e.g. [1♡] or [A♣] """
        return f"[{self.get_value(False)}{self.suit.value[1]}]"

    # --- Private methods ---


class Deck:
    """ Class that represents classic deck with 4 suits and cards in each suite from 1 to
    ace.
    """
    MAX_DECK_SIZE = len(Card.VALUES) * len(Suit)

    def __init__(self):
        self._cards = []
        self.fill()

    def __len__(self):
        return len(self._cards)

    # --- Properties ---

    @property
    def empty(self) -> bool:
        return len(self._cards) == 0

    # --- Public methods ---

    def fill(self):
        """ Restocks the deck with full deck"""
        self._cards.clear()
        
        value_range = range(Card.MIN_VALUE, len(Card.VALUES) + Card.MIN_VALUE)
        for suit, value in itertools.product(Suit, value_range):
            self._cards.append(Card(suit, value))

    def shuffle(self, times: int = 1):
        """ Shuffles the current decks cards given amount of times or once if given times
        is less than 1.
        """
        if not isinstance(times, int):
            raise ValueError('Invalid times parameter')
        if times < 1:
            raise ValueError('Deck must be shuffled atleast 1 time')
        for _ in range(times):
            random.shuffle(self._cards)

    def peek_top(self) -> Card:
        """ Peeks at the top card of the deck """
        return self._cards[-1]

    def get_card(self) -> Union[Card, None]:
        """ Removes the top most card from the deck and returns it """
        if len(self._cards) > 0:
            return self._cards.pop()
        return None

    def get_cards(self, cards: int) -> Sequence[Card]:
        """ Removes the top most cards from the deck and returns them in a list or one 
        card if given cards is less than 1. If deck does not have given amount of cards
        return rest of the cards.
        """
        if not isinstance(cards, int):
            raise ValueError('Invalid cards parameter')
        if cards < 1:
            cards = 1
        card_list = []
        for _ in range(cards):
            if len(self._cards) > 0:
                card_list.append(self._cards.pop())
            else:
                break
        return card_list