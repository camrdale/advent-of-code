import string

from aoc.map import ParsedMap, Coordinate


class ReverseHeightMap(ParsedMap):
    """A height map designed to be traversed in reverse, from ending to starting position."""
    def __init__(self, input: list[str]):
        super().__init__(input, string.ascii_lowercase + 'SE')
        self.starting_position = next(iter(self.features['S']))
        self.ending_position = next(iter(self.features['E']))
        self.features['a'].add(self.starting_position)
        self.features['z'].add(self.ending_position)
        self.heights: dict[Coordinate, str] = {}
        for height in string.ascii_lowercase:
            for location in self.features[height]:
                self.heights[location] = height

    def at_location(self, coordinate: Coordinate) -> str:
        return self.heights[coordinate]
    
    def neighbors(self, location: Coordinate) -> list['Coordinate']:
        height = ord(self.at_location(location))
        # Only include neighbors above or one height below, since this is reversed.
        # This means in the normal direction, the path will only climb to one height above.
        return [neighbor for neighbor in location.neighbors()
                if self.valid(neighbor) and ord(self.at_location(neighbor)) >= height - 1]
