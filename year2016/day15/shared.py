import re
from typing import NamedTuple, Self


DISC = re.compile(r'Disc #([0-9]*) has ([0-9]*) positions; at time=0, it is at position ([0-9]*).')


class Disc(NamedTuple):
    num: int
    positions: int
    time0_position: int

    @classmethod
    def from_text(cls, text: str) -> Self:
        match = DISC.match(text)
        assert match is not None, text
        return cls(*map(int, match.groups()))

    @staticmethod
    def button_time(discs: list['Disc']) -> int:
        t = 0
        increment = 1
        while discs:
            curr_disc = discs.pop(0)
            while (curr_disc.time0_position + t + curr_disc.num) % curr_disc.positions != 0:
                t += increment
            increment *= curr_disc.positions
        return t
