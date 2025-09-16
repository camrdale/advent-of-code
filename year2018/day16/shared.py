from abc import ABC, abstractmethod
import re
from typing import NamedTuple, Self

from aoc.input import InputParser


BEFORE = re.compile(r'Before: \[([0-9-]*), ([0-9-]*), ([0-9-]*), ([0-9-]*)\]')
OPERATION = re.compile(r'([0-9-]*) ([0-9-]*) ([0-9-]*) ([0-9-]*)')
AFTER = re.compile(r'After:  \[([0-9-]*), ([0-9-]*), ([0-9-]*), ([0-9-]*)\]')


class Sample(NamedTuple):
    before: dict[int, int]
    operation: list[int]
    after: dict[int, int]

    @classmethod
    def from_input(cls, parser: InputParser) -> list[Self]:
        input = parser.get_multipart_parsed_input(BEFORE, OPERATION, AFTER)
        samples: list[Self] = []
        for sample in input:
            if BEFORE not in sample:
                continue
            before: dict[int, int] = dict(enumerate(map(int, sample[BEFORE])))
            operation: list[int] = list(map(int, sample[OPERATION]))
            after: dict[int, int] = dict(enumerate(map(int, sample[AFTER])))
            samples.append(cls(before, operation, after))
        return samples
    
    def opcode(self) -> int:
        return self.operation[0]

    def test_operations(self, operations: list[type[Operation]]) -> list[type[Operation]]:
        ops: list[type[Operation]] = []
        for operation in operations:
            registers = dict(self.before)
            try:
                operation(self.operation[1], self.operation[2], self.operation[3]).apply(registers)
            except Exception:
                continue
            if registers == self.after:
                ops.append(operation)
        return ops


class Operation(ABC):
    def __init__(self, a: int, b: int, c: int) -> None:
        self.a = a
        self.b = b
        self.c = c

    @abstractmethod
    def apply(self, registers: dict[int, int]) -> None:
        """Apply the operation to the current registers."""
        pass

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.a}, {self.b}, {self.c})'


class ADDR(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = registers[self.a] + registers[self.b]


class ADDI(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = registers[self.a] + self.b


class MULR(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = registers[self.a] * registers[self.b]


class MULI(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = registers[self.a] * self.b


class BANR(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = registers[self.a] & registers[self.b]


class BANI(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = registers[self.a] & self.b


class BORR(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = registers[self.a] | registers[self.b]


class BORI(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = registers[self.a] | self.b


class SETR(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = registers[self.a]


class SETI(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = self.a


class GTIR(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = 1 if self.a > registers[self.b] else 0


class GTRI(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = 1 if registers[self.a] > self.b else 0


class GTRR(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = 1 if registers[self.a] > registers[self.b] else 0


class EQIR(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = 1 if self.a == registers[self.b] else 0


class EQRI(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = 1 if registers[self.a] == self.b else 0


class EQRR(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = 1 if registers[self.a] == registers[self.b] else 0


OPERATIONS: list[type[Operation]] = [
    ADDR, ADDI,
    MULR, MULI,
    BANR, BANI,
    BORR, BORI,
    SETR, SETI,
    GTIR, GTRI, GTRR,
    EQIR, EQRI, EQRR]
