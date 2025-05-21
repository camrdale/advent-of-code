import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


STARTING_POSITION = re.compile(r'Player ([12]) starting position: ([0-9]*)')


class DeterministicDice:
    def __init__(self, input: list[str]) -> None:
        self.positions = [0, 0]
        match = STARTING_POSITION.match(input[0])
        assert match is not None
        self.positions[0] = int(match.group(2))
        match = STARTING_POSITION.match(input[1])
        assert match is not None
        self.positions[1] = int(match.group(2))
        self.scores = [0, 0]
        self.next_die = 1
        self.num_rolls = 0
        self.player = 0

    def roll(self) -> int:
        roll = self.next_die
        self.next_die = (self.next_die % 100) + 1
        roll += self.next_die
        self.next_die = (self.next_die % 100) + 1
        roll += self.next_die
        self.next_die = (self.next_die % 100) + 1
        self.num_rolls += 3
        return roll

    def take_turn(self) -> int:
        """Take the next player's turn. Returns that players score after the turn."""
        roll = self.roll()
        self.positions[self.player] = ((self.positions[self.player] - 1) + roll) % 10 + 1
        self.scores[self.player] += self.positions[self.player]
        score = self.scores[self.player]
        log.log(log.DEBUG, f'Player {self.player+1} rolls {roll} and moves to space {self.positions[self.player]} for a total score of {score}')
        self.player = 1 - self.player
        return score


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        dirac = DeterministicDice(input)

        while dirac.take_turn() < 1000:
            pass

        losing_score = min(dirac.scores)
        log.log(log.RESULT, f'The losing score is {losing_score} and die was rolled {dirac.num_rolls} times: {losing_score*dirac.num_rolls}')
        return losing_score*dirac.num_rolls


part = Part1()

part.add_result(739785, """
Player 1 starting position: 4
Player 2 starting position: 8
""")

part.add_result(675024)
