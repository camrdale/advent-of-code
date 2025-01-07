from collections import defaultdict
import functools
from typing import NamedTuple, Any

from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part

CARD_VALUES = {str(d): d for d in range(2, 10)}
CARD_VALUES['T'] = 10
CARD_VALUES['J'] = 11
CARD_VALUES['Q'] = 12
CARD_VALUES['K'] = 13
CARD_VALUES['A'] = 14


class Card(NamedTuple):
    label: str

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, type(self)): 
            return NotImplemented
        return CARD_VALUES[self.label] < CARD_VALUES[other.label]
    
    def __str__(self) -> str:
        return self.label


class Hand(NamedTuple):
    cards: tuple[Card, Card, Card, Card, Card]

    @classmethod
    def from_string(cls, s: str) -> 'Hand':
        assert len(s) == 5
        return cls((Card(s[0]), Card(s[1]), Card(s[2]), Card(s[3]), Card(s[4])))

    @functools.cache
    def counts(self) -> dict[Card, int]:
        counts: dict[Card, int] = defaultdict(int)
        for card in self.cards:
            counts[card] += 1
        return counts

    @functools.cache
    def num_labels(self) -> int:
        return len(self.counts())

    @functools.cache
    def largest_group(self) -> int:
        return max(self.counts().values())

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, type(self)): 
            return NotImplemented
        if self.num_labels() != other.num_labels():
            return self.num_labels() > other.num_labels()
        if self.largest_group() != other.largest_group():
            return self.largest_group() < other.largest_group()
        return self.cards < other.cards
    
    def __str__(self) -> str:
        return ''.join(str(c) for c in self.cards)


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        hands: list[tuple[Hand, int]] = [
            (Hand.from_string(line[0]), int(line[1]))
            for line in parser.get_split_input()]
        hands.sort()

        total_winnings = 0
        for i, (hand, bid) in enumerate(hands):
            log(INFO, f'Hand {hand} has rank {i+1} and bid {bid}')
            total_winnings += (i+1) * bid

        log(RESULT, f'The total winnings: {total_winnings}')
        return total_winnings


part = Part1()

part.add_result(6440, """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""")

part.add_result(249483956)
