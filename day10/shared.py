from typing import NamedTuple
from collections.abc import Generator, Iterable


class Offset(NamedTuple):
    x: int
    y: int


NEIGHBORS = [
    Offset(0, -1),
    Offset(1, 0),
    Offset(0, 1),
    Offset(-1, 0)]


class Coordinate(NamedTuple):
    x: int
    y: int
    
    def add(self, offset: Offset) -> 'Coordinate':
        return Coordinate(self.x + offset.x, self.y + offset.y)
    
    def valid(self, width: int, height: int) -> bool:
        return 0 <= self.x < width and 0 <= self.y < height


class TopographicMap:
    def __init__(self, lines: Iterable[str]):
        self.altitudes: dict[Coordinate, int] = {}
        self.height = 0
        self.width = 0
        for y, line in enumerate(lines):
            if len(line.strip()) > 0:
                self.width = len(line.strip())
                self.height += 1
                for x, c in enumerate(line.strip()):
                    self.altitudes[Coordinate(x,y)] = int(c)

    def trailheads(self) -> Generator[Coordinate]:
        for y in range(self.height):
            for x in range(self.width):
                coord = Coordinate(x,y)
                if self.altitudes.get(coord) == 0:
                    yield coord

    def score(self, trailhead: Coordinate) -> int:
        """Calculate the score of the trailhead."""
        altitude = 0
        coords = set([trailhead])
        while altitude < 9 and len(coords) > 0:
            next_coords: set[Coordinate] = set()
            for coord in coords:
                for offset in NEIGHBORS:
                    next_coord = coord.add(offset)
                    if next_coord.valid(self.width, self.height) and self.altitudes[next_coord] == altitude + 1:
                        next_coords.add(next_coord)
            coords = next_coords
            altitude += 1
        # for coord in coords:
        #     print('  Found a path from', starting_coord, 'to', coord)
        return len(coords)

    def rating(self, trailhead: Coordinate) -> int:
        """Calculate the rating of the trailhead."""
        altitude = 0
        coords = [trailhead]
        while altitude < 9 and len(coords) > 0:
            next_coords: list[Coordinate] = []
            for coord in coords:
                for offset in NEIGHBORS:
                    next_coord = coord.add(offset)
                    if next_coord.valid(self.width, self.height) and self.altitudes[next_coord] == altitude + 1:
                        next_coords.append(next_coord)
            coords = next_coords
            altitude += 1
        # for coord in coords:
        #     print('  Found a path from', starting_coord, 'to', coord)
        return len(coords)
