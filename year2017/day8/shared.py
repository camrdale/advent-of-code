from collections.abc import Callable
import operator
import re
from typing import NamedTuple, Self


INSTRUCTION = re.compile(r'([a-z]*) (inc|dec) ([0-9-]*) if ([a-z]*) (<|>|<=|>=|==|!=) ([0-9-]*)')

OPERATORS: dict[str, Callable[[int, int], int]] = {
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
    '==': operator.eq,
    '!=': operator.ne
}


class Instruction(NamedTuple):
    register: str
    increment: int
    condition_register: str
    condition_operator: Callable[[int, int], int]
    condition_value: int

    @classmethod
    def from_text(cls, text: str) -> Self:
        match = INSTRUCTION.match(text)
        assert match is not None, text
        return cls(
            match.group(1),
            int(match.group(3)) * (-1 if match.group(2) == 'dec' else 1),
            match.group(4),
            OPERATORS[match.group(5)],
            int(match.group(6)))
    
    def apply(self, registers: dict[str, int]) -> int | None:
        if self.condition_operator(registers[self.condition_register], self.condition_value):
            registers[self.register] += self.increment
            return registers[self.register]
