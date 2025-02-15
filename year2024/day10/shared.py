from collections.abc import Generator

from aoc.log import log, DEBUG
from aoc.map import Coordinate, NEIGHBORS, ParsedMap


class TopographicMap(ParsedMap):
    def __init__(self, lines: list[str]):
        super().__init__(lines, '0123456789')

    def trailheads(self) -> Generator[Coordinate]:
        for coord in self.features['0']:
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
                    if self.valid(next_coord) and next_coord in self.features[str(altitude + 1)]:
                        next_coords.add(next_coord)
            coords = next_coords
            altitude += 1
        for coord in coords:
            log(DEBUG, '  Found a path from', trailhead, 'to', coord)
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
                    if self.valid(next_coord) and next_coord in self.features[str(altitude + 1)]:
                        next_coords.append(next_coord)
            coords = next_coords
            altitude += 1
        for coord in coords:
            log(DEBUG, '  Found a path from', trailhead, 'to', coord)
        return len(coords)
