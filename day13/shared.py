import re
from collections.abc import Iterable
from typing import NamedTuple

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


def parse(input: Iterable[str]) -> list[Machine]:
    machines: list[Machine] = []
    xa = 0
    xb = 0
    x = 0
    ya = 0
    yb = 0
    y = 0
    for line in input:
        if line.strip() == '':
            continue
        if match := BUTTON_A.match(line):
            xa, ya = int(match.group(1)), int(match.group(2))
        elif match := BUTTON_B.match(line):
            xb, yb = int(match.group(1)), int(match.group(2))
        elif match := PRIZE.match(line):
            x, y = int(match.group(1)), int(match.group(2))
            machines.append(Machine(xa, ya, xb, yb, x, y))
    return machines


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
