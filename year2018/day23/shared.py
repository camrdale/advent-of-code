import re
from typing import NamedTuple, Self

from aoc.map import Coordinate3D

from aoc.range import Range

NANOBOT = re.compile(r'pos=<([0-9,-]*)>, r=([0-9]*)')


class Nanobot(NamedTuple):
    radius: int
    location: Coordinate3D

    @classmethod
    def from_text(cls, text: str) -> Self:
        match = NANOBOT.match(text)
        assert match is not None, text
        return cls(int(match.group(2)), Coordinate3D.from_text(match.group(1)))

    def in_range(self, location: Coordinate3D) -> bool:
        return self.location.difference(location).manhattan_distance() <= self.radius

    def ranges(self) -> tuple[Range, Range, Range]:
        return (
            Range.closed(self.location.location.x - self.radius, self.location.location.x + self.radius),
            Range.closed(self.location.location.y - self.radius, self.location.location.y + self.radius),
            Range.closed(self.location.z - self.radius, self.location.z + self.radius),
        )


