from collections import defaultdict
import re
from typing import NamedTuple, Self

import cachetools

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


STARTING_POSITION = re.compile(r'Player ([12]) starting position: ([0-9]*)')

MAX_CACHE_SIZE = 200000000


class DiracState(NamedTuple):
    positions: tuple[int, int]
    scores: tuple[int, int]

    @classmethod
    def initial_state(cls, starting_positions: tuple[int, int]) -> Self:
        return cls(starting_positions, (0, 0))

    def next_state(self, roll: int) -> 'DiracState':
        position = ((self.positions[0] - 1) + roll) % 10 + 1
        score = self.scores[0] + position
        # Player whose turn it is, is always first in the tuples
        return DiracState((self.positions[1], position), (self.scores[1], score))


class DiracWins(NamedTuple):
    player_1: int
    player_2: int

    def times(self, multiplier: int) -> 'DiracWins':
        return DiracWins(self.player_1 * multiplier, self.player_2 * multiplier)
    
    def add(self, other: 'DiracWins') -> 'DiracWins':
        return DiracWins(self.player_1 + other.player_1, self.player_2 + other.player_2)
    
    def reverse(self) -> 'DiracWins':
        return DiracWins(self.player_2, self.player_1)


class DiracDice:
    def __init__(self, input: list[str]) -> None:
        match1 = STARTING_POSITION.match(input[0])
        assert match1 is not None
        match2 = STARTING_POSITION.match(input[1])
        assert match2 is not None
        self.starting_positions = int(match1.group(2)), int(match2.group(2))
        self.cache: cachetools.LRUCache[tuple[str], int] = cachetools.LRUCache(maxsize=MAX_CACHE_SIZE)
        # Mapping of sum of 3 rolls to number of times that sum occurs
        self.rolls: dict[int, int] = defaultdict(int)
        for roll_1 in range(1, 4):
            for roll_2 in range(1, 4):
                for roll_3 in range(1, 4):
                    self.rolls[roll_1 + roll_2 + roll_3] += 1

    @cachetools.cachedmethod(lambda self: self.cache)
    def _num_universes(self, state: DiracState) -> DiracWins:
        if state.scores[1] >= 21:
            return DiracWins(0, 1)

        wins = DiracWins(0, 0)
        for roll, occurrences in self.rolls.items():
            wins = wins.add(self._num_universes(state.next_state(roll)).times(occurrences))

        # Reverse because the players swap posiions on each roll
        return wins.reverse()

    def num_universes(self) -> int:
        return max(self._num_universes(DiracState.initial_state(self.starting_positions)))


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        dirac = DiracDice(input)

        most_wins = dirac.num_universes()

        log.log(log.RESULT, f'The most winning player wins in universes: {most_wins}')
        return most_wins


part = Part2()

part.add_result(444356092776315, """
Player 1 starting position: 4
Player 2 starting position: 8
""")

part.add_result(570239341223618)
