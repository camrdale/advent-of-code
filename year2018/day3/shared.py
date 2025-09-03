import re
from typing import NamedTuple, Self

import numpy
import numpy.typing


CLAIM = re.compile(r'#([0-9]*) @ ([0-9]*),([0-9]*): ([0-9]*)x([0-9]*)')


class Claim(NamedTuple):
    id: int
    start_x: int
    start_y: int
    size_x: int
    size_y: int

    @classmethod
    def from_text(cls, text: str) -> Self:
        match = CLAIM.match(text)
        assert match is not None
        return cls(*map(int, match.groups()))
    
    @classmethod
    def sum(cls, claims: list[Claim]) -> numpy.typing.NDArray[numpy.uint8]:
        size_x = max(claim.start_x + claim.size_x for claim in claims)
        size_y = max(claim.start_y + claim.size_y for claim in claims)

        fabric = numpy.zeros((size_x, size_y), dtype=numpy.uint8)
        for claim in claims:
            fabric[claim.area()] += 1

        return fabric
    
    def area_x(self) -> slice[int, int, int]:
        return slice(self.start_x, self.start_x + self.size_x)
    
    def area_y(self) -> slice[int, int, int]:
        return slice(self.start_y, self.start_y + self.size_y)

    def area(self) -> tuple[slice[int, int, int], slice[int, int, int]]:
        return self.area_x(), self.area_y()
