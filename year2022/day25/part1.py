import enum
from typing import NamedTuple, Any, Self

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class SnafuDigit(enum.Enum):
    DOUBLE_MINUS = ('=', -2)
    MINUS = ('-', -1)
    ZERO = ('0', 0)
    ONE = ('1', 1)
    TWO = ('2', 2)

    def __new__(cls, *values: Any):
        obj = object.__new__(cls)
        # First value is canonical value
        obj._value_ = values[0]
        # Second value can also be used for creation of enums
        cls._value2member_map_[values[1]] = obj
        return obj
    
    def __init__(self, digit: str, integer: int):
        self.digit = digit
        self.integer = integer


class SnafuNumber(NamedTuple):
    # Digits in reverse order, from least significant to most significant.
    digits: tuple[SnafuDigit, ...]

    @classmethod
    def from_text(cls, text: str) -> Self:
        return cls(tuple(SnafuDigit(c) for c in reversed(text)))
    
    @classmethod
    def from_int(cls, value: int) -> Self:
        digits: list[SnafuDigit] = []

        while value != 0:
            value, remainder = divmod(value, 5)
            if remainder > 2:
                remainder -= 5
                value += 1
            digits.append(SnafuDigit(remainder))

        return cls(tuple(digits))

    def __repr__(self) -> str:
        return ''.join(digit.digit for digit in reversed(self.digits))
    
    def to_int(self) -> int:
        value = 0
        for i, digit in enumerate(self.digits):
            value += 5**i * digit.integer
        return value
    
    def add(self, other: 'SnafuNumber') -> 'SnafuNumber':
        digits: list[SnafuDigit] = []

        
        return SnafuNumber(tuple(digits))


class Part1(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()

        log.log(log.INFO, f"{'SNAFU':>20} {'Decimal':>15}")
        snafu_sum = 0
        for line in input:
            snafu = SnafuNumber.from_text(line)
            snafu_sum += snafu.to_int()
            log.log(log.INFO, f'{str(snafu):>20} {snafu.to_int():>15}')

        snafu = SnafuNumber.from_int(snafu_sum)

        log.log(log.RESULT, f'The sum of the SNAFU numbers: {snafu} (in decimal: {snafu_sum})')
        return str(snafu)


part = Part1()

part.add_result('2=-1=0', r"""
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
""")

part.add_result('2=--00--0220-0-21==1')
