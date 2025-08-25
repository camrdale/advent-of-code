import re
from typing import NamedTuple, Self

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


STARTING_STATE = re.compile(r'Begin in state ([A-Z]).')
CHECKSUM = re.compile(r'Perform a diagnostic checksum after ([0-9]*) steps.')
STATE = re.compile(r'In state ([A-Z]):')
VALUE = re.compile(r'  If the current value is (0|1):')
WRITE = re.compile(r'    - Write the value (0|1).')
MOVE = re.compile(r'    - Move one slot to the (left|right).')
NEXT_STATE = re.compile(r'    - Continue with state ([A-Z]).')
TAPE_BLOCK = 128


class ValueDefinition(NamedTuple):
    value: int
    write: int  # 0 or 1
    move: int  # -1 for left, 1 for right
    next_state: str  # A - Z

    @classmethod
    def from_text(cls, text: list[str]) -> Self:
        match = VALUE.match(text[0])
        assert match is not None, text
        value = int(match.group(1))
        match = WRITE.match(text[1])
        assert match is not None, text
        write = int(match.group(1))
        match = MOVE.match(text[2])
        assert match is not None, text
        move = -1 if match.group(1) == 'left' else 1
        match = NEXT_STATE.match(text[3])
        assert match is not None, text
        next_state = match.group(1)
        return cls(value, write, move, next_state)


class StateDefinition(NamedTuple):
    state: str
    value_0: ValueDefinition
    value_1: ValueDefinition

    @classmethod
    def from_text(cls, text: list[str]) -> Self:
        match = STATE.match(text[0])
        assert match is not None, text
        state = match.group(1)
        value_0 = ValueDefinition.from_text(text[1:5])
        assert value_0.value == 0
        value_1 = ValueDefinition.from_text(text[5:])
        assert value_1.value == 1
        return cls(state, value_0, value_1)


class TuringMachine:
    def __init__(self, input: list[list[str]]) -> None:
        match = STARTING_STATE.match(input[0][0])
        assert match is not None, input[0]
        self.starting_state = match.group(1)
        match = CHECKSUM.match(input[0][1])
        assert match is not None, input[0]
        self.checksum_steps = int(match.group(1))

        self.states: dict[str, StateDefinition] = {}
        for section in input[1:]:
            state = StateDefinition.from_text(section)
            self.states[state.state] = state
        
        self.tape = [0] * (TAPE_BLOCK * 2)
        self.cursor = TAPE_BLOCK

    def get_value(self) -> int:
        try:
            return self.tape[self.cursor]
        except IndexError:
            pass
        if self.cursor < 0:
            self.tape = [0]*TAPE_BLOCK + self.tape
            self.cursor += TAPE_BLOCK
        else:
            self.tape.extend([0]*TAPE_BLOCK)
        return 0

    def run(self) -> int:
        state = self.states[self.starting_state]
        for _ in range(self.checksum_steps):
            value = state.value_0 if self.get_value() == 0 else state.value_1
            self.tape[self.cursor] = value.write
            self.cursor += value.move
            state = self.states[value.next_state]

        return sum(self.tape)


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input: list[list[str]] = parser.get_multipart_input()

        machine = TuringMachine(input)

        checksum = machine.run()

        log.log(log.RESULT, f'The checksum after {machine.checksum_steps:,} steps: {checksum}')
        return checksum


part = Part1()

part.add_result(3, """
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
""")

part.add_result(4230)
