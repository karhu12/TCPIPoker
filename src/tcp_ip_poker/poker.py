from __future__ import annotations
from typing import Union, Sequence, Tuple
import enum, itertools, random, copy

class Suit(enum.Enum):
    """ Value is a tuple of description and unicode symbol """
    SPADES = ('Spades', '♤')
    CLUBS = ('Clubs','♣')
    HEARTS = ('Hearts','♡')
    DIAMONDS = ('Diamonds','♢')

    @classmethod
    def index(cls, item: Suit):
        for idx, suit in enumerate(cls):
            if suit == item:
                return idx
        return -1

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

    def __eq__(self, card: Card) -> bool:
        return self.value == card.value and self.suit == card.suit

    def __lt__(self, card: Card) -> bool:
        return  self.value < card.value

    def __gt__(self, card: Card) -> bool:
        return  self.value > card.value

    def __str__(self) -> str:
        return self.get_short_string()

    def __add__(self, card: Card) -> int:
        return self.value + card.value

    def __sub__(self, card: Card) -> int:
        return self.value - card.value
        
    def __hash__(self):
        return (self.value << 2) | Suit.index(self.suit)

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

    def get_long_string(self) -> str:
        """ Returns the long version from card e.g. "Ace of Hearts ♡" """
        return f"{self.get_value()} of {self.suit.value[0]} {self.suit.value[1]}"

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
        """ Returns an copy from top most card on the deck """
        return copy.copy(self._cards[-1])

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

class Player:
    """ Represents a single player in a game of poker. Host is the IP address of given 
    player but it can also be 'AIx' which represent an offline player.
    """
    MAX_CARDS_HAND = 5

    def __init__(self, host: str):
        self._host = host
        self._hand: Sequence[Card] = []

    # --- Properties ---

    @property
    def host(self) -> str:
        return self._host

    @property
    def hand(self) -> Sequence[Card]:
        """ Returns copy of current hand as a list of cards"""
        return copy.copy(self._hand)

    @property
    def hand_full(self) -> bool:
        """ Returns boolean whether the players hand is full or not """
        return len(self._hand) == self.MAX_CARDS_HAND

    # --- Public methods ---

    def pick_card(self, card: Card):
        if self.hand_full:
            raise Exception('Hand is full')
        self._hand.append(card)

    def discard_card(self, card: Union[int, Card]) -> Card:
        """ Discards the card of given index from hand. """
        if isinstance(card, Card):
            card = self._hand.index(card)
        elif not -1 < card < len(self._hand):
            raise ValueError('Invalid card index')
        return self._hand.pop(card)

    def discard_cards(self) -> Sequence[Card]:
        """ Discards all cards in hand """
        cards = []
        while self.hand_full:
            cards.append(self._hand.pop())
        return cards

class VictoryCombination(enum.Enum):
    HIGH_CARD = 0
    PAIR = enum.auto()
    TWO_PAIRS = enum.auto()
    THREE_OF_A_KIND = enum.auto()
    STRAIGHT = enum.auto()
    FLUSH = enum.auto()
    FULL_HOUSE = enum.auto()
    FOUR_OF_A_KIND = enum.auto()
    STRAIGHT_FLUSH = enum.auto()

    @classmethod
    def determine_best_combination(
            cls,
            cards: Sequence[Card]
        ) -> Tuple(VictoryCombination, Sequence[Card]):
        best = VictoryCombination.HIGH_CARD
        combinations = [list(comb) for comb in itertools.combinations(cards, r=5)]
        for combination in combinations:
            combination.sort(key=lambda item: item.value)
            flush = VictoryCombination.is_flush(combination)
            straight = VictoryCombination.is_straight(combination)
            duplicates = VictoryCombination.duplicate_value_cards(combination)
            full_house = VictoryCombination.is_full_house(duplicates)
            pairs, kinds,  = VictoryCombination.multiples(duplicates)
            
            if straight and flush:
                best = VictoryCombination.compare_combinations(best, VictoryCombination.STRAIGHT_FLUSH)
            elif kinds == 4:
                best = VictoryCombination.compare_combinations(best,  VictoryCombination.FOUR_OF_A_KIND)
            elif full_house:
                best = VictoryCombination.compare_combinations(best, VictoryCombination.FULL_HOUSE)
            elif flush:
                best = VictoryCombination.compare_combinations(best, VictoryCombination.FLUSH)
            elif straight:
                best = VictoryCombination.compare_combinations(best, VictoryCombination.STRAIGHT)
            elif kinds == 3:
                best = VictoryCombination.compare_combinations(best, VictoryCombination.THREE_OF_A_KIND)
            elif pairs == 2:
                best = VictoryCombination.compare_combinations(best, VictoryCombination.TWO_PAIRS)
            elif pairs == 1:
                best = VictoryCombination.compare_combinations(best, VictoryCombination.PAIR)
        return best

    @classmethod
    def compare_combinations(cls, c1: VictoryCombination, c2: VictoryCombination):
        """ Returns the combination of higher degree. """
        return c1 if c1.value > c2.value else c2

    @staticmethod
    def is_flush(cards: Sequence[Card]):
        """ Returns boolean whether the given cards contain a flush """
        for suit in Suit:
            suit_count = sum(1 for c in cards if c.suit == suit)
            if suit_count == 5:
                return True
        return False

    @staticmethod
    def is_straight(cards: Sequence[Card]):
        """ Returns boolean whether the given cards contain a straight """
        total_diff = 0
        for idx, card in enumerate(cards):
            if idx == 0:
                continue
            total_diff += card - cards[idx - 1]
        if total_diff == 4:
            return True
        return False

    @staticmethod
    def is_full_house(duplicates: Sequence[Card]):
        """ Return boolean whether the given cards contain a full house """
        two_type = False
        three_type = False
        for card_value in duplicates:
            card_len = len(duplicates[card_value])
            if card_len == 2:
                two_type = True
            elif card_len == 3:
                three_type = True
        return two_type and three_type

    @staticmethod
    def multiples(duplicates: Sequence[Card]) -> Tuple[int, int]:
        """ Returns how many pairs and cards of kind there are as a tuple """
        pairs = 0
        kinds = 0
        for card_value in duplicates:
            card_len = len(duplicates[card_value]) 
            if card_len == 2:
                pairs += 1
            kinds = max(kinds, len(duplicates[card_value]))
        return pairs, kinds

    @staticmethod
    def duplicate_value_cards(cards: Sequence[Card]) -> Sequence[Card]:
        """ Returns dict mapped with card value to the cards of that value """
        duplicates = {}
        for card in cards:
            if card.value not in duplicates:
                duplicates[card.value] = []
            duplicates[card.value].append(card)
        return duplicates

class PokerGame:
    """ Class represents a game of Poker between 2 to 4 players. Players can either be 
    controller by AI of the software.
    """
    MINIMUM_PLAYERS = 2
    MAXIMUM_PLAYERS = 4

    def __init__(self):
        self._deck = Deck()
        self._table: Sequence[Card] = []
        self._discard_pile: Sequence[Card] = []
        self._players: Sequence[Player] = []
        self._moves: Sequence[Tuple[Player, Card]]
        self._active = False
        self._players_turn: Union[Player, None] = None
        self._players_turn_handled: Sequence[Player] = []
        self._current_turn = 0
        self._played = 0

    # --- Properties ---

    @property
    def active(self) -> bool:
        return self._started

    @property
    def players(self) -> Sequence[Player]:
        """ Returns an copy of current players """
        return copy.copy(self._players)

    @property
    def table(self) -> Sequence[Card]:
        """ Returns an copy of current tables cards """
        return copy.copy(self._table)

    # --- Public methods ---

    def start(self):
        if self.active:
            raise Exception('Game already started')
        if len(self._players) < 2:
            raise Exception('Poker game requires atleast 2 playeres')
        if self._played > 0:
            pass # change leader
        self._active = True
        self._deck.shuffle(3)
        self._handle_next_turn()

    def check(self, player: Player):
        if self._players_turn == player:
            self._players_turn = self._players[(self._players.index(player) + 1) % len(self._players)]
            
        else:
            raise Exception(f'Not {player}s turn')


    def replace_cards(
            self,
            player: Player,
            cards: Union[Card, int, Sequence[Union[Card, int]]]
        ):
        if self._players_turn == player:
            pass
        else:
            raise Exception(f'Not {player}s turn')

    

    def add_player(self, host: Union[str, None] = None):
        """ Adds a new player to the game with given host address. If host is None the 
        player will be NPC (Non player controller) player.
        """
        if len(self._players) == self.MAXIMUM_PLAYERS:
            raise Exception('Game already has maximum number of players')
        new = Player(host)
        for player in self._players:
            if player.host == new:
                raise Exception('Player already exists in the current game')
        self._players.append(new)

    # --- Private methods ---

    def _rotate_player(self, player: Player):
        self._players_turn_handled.append(player)
        if len(self._players_turn_handled) == len(self._players):
            self._players_turn_handled.clear()
            self._handle_next_turn()
        else:
            self._players_turn = self._players[(self._players.index(player) + 1) % len(self._players)]

    def _handle_next_turn(self):
        if self._current_turn == 0:
            self._serve_cards_to_players(2)
            self._serve_cards_to_table(3)
        elif self._current_turn == 1:
            self._serve_cards_to_table(1)
        elif self._current_turn == 2:
            self._serve_cards_to_table(1)
        else:
            self._handle_winner()
        self._players_turn = self._players[0]
        self._current_turn += 1

    def _serve_cards_to_players(self, count: int):
        for _ in range(count):
            for player in self._players:
                player.pick_card(self._deck.get_card())

    def _serve_cards_to_table(self, count: int):
        for card in self._deck.get_cards(count):
            self._table.append(card)

    def _handle_winner():
        pass