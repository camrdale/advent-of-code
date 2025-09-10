from collections.abc import Iterable
import re
from typing import NamedTuple, Self

from aoc import log
from aoc.map import Coordinate, Offset


STAR = re.compile(r'position=<[ ]*([0-9-]*),[ ]*([0-9-]*)> velocity=<[ ]*([0-9-]*),[ ]*([0-9-]*)>')


class Star(NamedTuple):
    position: Coordinate
    velocity: Offset

    @classmethod
    def from_text(cls, text: str) -> Self:
        match = STAR.match(text)
        assert match is not None
        return cls(Coordinate(*map(int, match.group(1, 2))), Offset(*map(int, match.group(3, 4))))

    def position_at_time(self, time: int) -> Coordinate:
        return self.position.add(self.velocity.times(time))


class Dimensions(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    @classmethod
    def from_positions(cls, positions: Iterable[Coordinate]) -> Self:
        return cls(
            min(position.x for position in positions),
            max(position.x for position in positions),
            min(position.y for position in positions),
            max(position.y for position in positions))

    def size(self) -> int:
        return min((self.max_x - self.min_x + 1), (self.max_y - self.min_y + 1))


class StarField:
    def __init__(self, input: list[str]) -> None:
        self.stars: list[Star] = []
        for line in input:
            self.stars.append(Star.from_text(line))
        
    def positions_at_time(self, time: int) -> set[Coordinate]:
        return set([star.position_at_time(time) for star in self.stars])
        
    def dimensions(self, time: int) -> Dimensions:
        return Dimensions.from_positions(self.positions_at_time(time))

    def size_rate_of_change(self, time: int) -> int:
        return self.dimensions(time + 1).size() - self.dimensions(time).size()

    def time_to_converge(self, time: int) -> float:
        size = self.dimensions(time).size()
        rate_of_change = self.dimensions(time + 1).size() - size
        return -size / rate_of_change

    def converge(self) -> int:
        time = 0
        dimensions = Dimensions.from_positions(self.positions_at_time(time))

        while True:
            log.log(log.INFO, f'At time {time} star field converges to dimensions: {dimensions}')

            time_delta = self.time_to_converge(time)
            if abs(time_delta) < 3:
                time_delta = -1 if time_delta < 0 else 1
            next_dimensions = Dimensions.from_positions(self.positions_at_time(time + int(time_delta)))
            if next_dimensions.size() > dimensions.size():
                log.log(log.INFO, f'At time {time + time_delta} star field would expand to dimension: {next_dimensions}')
                return time
            dimensions = next_dimensions
            time = time + int(time_delta)

    def print(self, time: int) -> str:
        positions = self.positions_at_time(time)
        dimensions = Dimensions.from_positions(positions)

        output = ''
        for y in range(dimensions.min_y, dimensions.max_y + 1):
            for x in range(dimensions.min_x, dimensions.max_x + 1):
                output += '\u2588' if Coordinate(x, y) in positions else ' '
            output += '\n'
        return output
