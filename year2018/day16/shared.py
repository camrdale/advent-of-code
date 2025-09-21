from collections.abc import Iterable
import re
from typing import NamedTuple, Self

from aoc.input import InputParser

from year2018.chronal import Operation


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

    def test_operations(self, operations: Iterable[type[Operation]]) -> list[type[Operation]]:
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
