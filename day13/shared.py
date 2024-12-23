import re
from typing import NamedTuple

from aoc.input import InputParser
from aoc.log import log, INFO


BUTTON_A = re.compile(r'Button A: X\+([0-9]*), Y\+([0-9]*)')
BUTTON_B = re.compile(r'Button B: X\+([0-9]*), Y\+([0-9]*)')
PRIZE = re.compile(r'Prize: X\=([0-9]*), Y\=([0-9]*)')


class Machine(NamedTuple):
    xa: int
    ya: int
    xb: int
    yb: int
    x: int
    y: int

    def __str__(self) -> str:
        return f'A: X+{self.xa}, Y+{self.ya}; B: X+{self.xb}, Y+{self.yb}; Prize: X={self.x}, Y={self.y}'


def parse(parser: InputParser) -> list[Machine]:
    return [
        Machine(int(parsed[BUTTON_A][0]), int(parsed[BUTTON_A][1]),
                int(parsed[BUTTON_B][0]), int(parsed[BUTTON_B][1]),
                int(parsed[PRIZE][0]), int(parsed[PRIZE][1]))
        for parsed in parser.get_multipart_parsed_input(BUTTON_A, BUTTON_B, PRIZE)]


def win(m: Machine) -> int | None:
    b_num = m.y*m.xa - m.x*m.ya
    b_denom = m.xa*m.yb - m.xb*m.ya
    if b_num % b_denom != 0:
        log(INFO, f'No solution for: {m}')
        return None
    b = b_num // b_denom

    a_num = m.y*m.xb - m.x*m.yb
    a_denom = m.xb*m.ya - m.xa*m.yb
    if a_num % a_denom != 0:
        log(INFO, f'No solution for: {m}')
        return None
    a = a_num // a_denom

    log(INFO, f'Optimal solution: {a}*{m.xa} + {b}*{m.xb} = {m.x}, {a}*{m.ya} + {b}*{m.yb} = {m.y}')
    return a*3 + b
