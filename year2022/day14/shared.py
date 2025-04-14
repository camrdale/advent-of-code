import itertools
import re

from aoc.map import UnknownMap, Coordinate, Offset


ROCK = '#'
SAND = 'o'
START = '+'
FALLING_DIRECTIONS = [Offset(0,1), Offset(-1,1), Offset(1,1)]


class CaveMap(UnknownMap):
    def __init__(self, input: list[str]):
        super().__init__(ROCK + SAND + START)
        self.add_feature(START, Coordinate(500,0))
        self.min_x, self.max_x = 500, 500
        self.last_path: list[Coordinate] = [Coordinate(500,0)]
        for line in input:
            coords = [Coordinate.from_text(s) for s in re.split(' -> ', line)]
            for start, end in itertools.pairwise(coords):
                direction = end.difference(start).to_direction()
                location = start
                self.add_feature(ROCK, location)
                while location != end:
                    location = location.add(direction)
                    self.add_feature(ROCK, location)

    def next_location(self, location: Coordinate) -> Coordinate | None:
        for direction in FALLING_DIRECTIONS:
            next_location = location.add(direction)
            if next_location not in self.features[ROCK] and next_location not in self.features[SAND]:
                return next_location

    def add_sand(self) -> bool:
        """Add a unit of sand, returning True if it can be added and comes to rest."""
        if not self.last_path:
            return False
        location = self.last_path.pop()
        while location.y <= self.max_y:
            next_location = self.next_location(location)
            if next_location is None:
                self.add_feature(SAND, location)
                return True
            self.last_path.append(location)
            location = next_location
        return False
