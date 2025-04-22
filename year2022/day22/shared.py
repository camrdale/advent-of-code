from collections import defaultdict
import re

from aoc import log
from aoc.map import Coordinate, ParsedMap, UP, DOWN, LEFT, RIGHT


WALL = '#'
OPEN = '.'

DIRECTIONS = [RIGHT, DOWN, LEFT, UP]

PATH_TILES = re.compile(r'[0-9]+')
PATH_TURN = re.compile(r'[RL]+')


class MonkeyMap(ParsedMap):
    def __init__(self, input: list[str]):
        super().__init__(input, WALL + OPEN)
        # Map of edge (location, direction) to connect to (location, direction).
        self.wraps: dict[tuple[Coordinate, int], tuple[Coordinate, int]] = {}
        self.direction: int = 0
        self.location: Coordinate = Coordinate(min(location.x for location in self.features[WALL].union(self.features[OPEN]) if location.y == 0), 0)
        log.log(log.DEBUG, f'Starting at location: {self.location}')
        self.path: dict[int, set[Coordinate]] = defaultdict(set)
        self.path[self.direction].add(self.location)

    def wrap(self, location: Coordinate, direction: int, new_location: Coordinate, new_direction: int):
        """Adds the edge mapping and the reverse."""
        self.wraps[location, direction] = new_location, new_direction
        self.wraps[new_location, (new_direction + 2) % 4] = location, ((direction + 2) % 4)

    def calculate_edge_wrapping(self):
        """Calculates edge mappings for simple wrapping."""
        all_locations = self.features[WALL].union(self.features[OPEN])
        min_x_for_row: dict[int, int] = defaultdict(lambda: self.max_x)
        max_x_for_row: dict[int, int] = defaultdict(int)
        min_y_for_column: dict[int, int] = defaultdict(lambda: self.max_y)
        max_y_for_column: dict[int, int] = defaultdict(int)
        for location in all_locations:
            min_x_for_row[location.y] = min(min_x_for_row[location.y], location.x)
            max_x_for_row[location.y] = max(max_x_for_row[location.y], location.x)
            min_y_for_column[location.x] = min(min_y_for_column[location.x], location.y)
            max_y_for_column[location.x] = max(max_y_for_column[location.x], location.y)
        for row in range(self.min_y, self.max_y + 1):
            self.wrap(Coordinate(max_x_for_row[row], row), 0, Coordinate(min_x_for_row[row], row), 0)
        for column in range(self.min_x, self.max_x + 1):
            self.wrap(Coordinate(column, max_y_for_column[column]), 1, Coordinate(column, min_y_for_column[column]), 1)

    def calculate_test_cube_wrapping(self):
        """Calculates wrapping around the example input cube."""
        for row in range(0, 4):
            self.wrap(Coordinate(11, row), 0, Coordinate(15, 11 - row), 2)
            self.wrap(Coordinate(8, row), 2, Coordinate(4 + row, 4), 1)
        for row in range(4, 8):
            self.wrap(Coordinate(11, row), 0, Coordinate(19 - row, 8), 1)
            self.wrap(Coordinate(0, row), 2, Coordinate(15 + 4 - row, 11), 3)
        for row in range(8, 12):
            self.wrap(Coordinate(8, row), 2, Coordinate(15 - row, 7), 3)
        for column in range(0,4):
            self.wrap(Coordinate(column, 4), 3, Coordinate(11 - column, 0), 1)
            self.wrap(Coordinate(column, 7), 1, Coordinate(11 - column, 11), 3)

    def calculate_final_cube_wrapping(self):
        """Calculates wrapping around the final input cube."""
        for row in range(0, 50):
            self.wrap(Coordinate(149, row), 0, Coordinate(99, 149 - row), 2)
            self.wrap(Coordinate(50, row), 2, Coordinate(0, 149 - row), 0)
        for row in range(50, 100):
            self.wrap(Coordinate(99, row), 0, Coordinate(100 + row - 50, 49), 3)
            self.wrap(Coordinate(50, row), 2, Coordinate(row - 50, 100), 1)
        for row in range(150, 200):
            self.wrap(Coordinate(49, row), 0, Coordinate(50 + row - 150, 149), 3)
            self.wrap(Coordinate(0, row), 2, Coordinate(50 + row - 150, 0), 1)
        for column in range(0, 50):
            self.wrap(Coordinate(column, 199), 1, Coordinate(100 + column, 0), 1)

    def move(self, tiles: int):
        for _ in range(tiles):
            if (self.location, self.direction) in self.wraps:
                new_location, new_direction = self.wraps[self.location, self.direction]
            else:
                new_location = self.location.add(DIRECTIONS[self.direction])
                new_direction = self.direction
            if new_location in self.features[WALL]:
                return
            if new_location not in self.features[OPEN]:
                raise ValueError(f'Pathed off the map! {self.location},{self.direction} -> {new_location},{new_direction}')
            self.location = new_location
            self.direction = new_direction
            self.path[self.direction].add(self.location)

    def turn(self, direction: str):
        self.path[self.direction].discard(self.location)
        if direction == 'R':
            self.direction = (self.direction + 1) % 4
        elif direction == 'L':
            self.direction = (self.direction - 1) % 4
        else:
            raise ValueError(f'Unexpected direction to turn: {direction}')
        self.path[self.direction].add(self.location)

    def final_password(self) -> int:
        return 1000 * (self.location.y + 1) + 4 * (self.location.x + 1) + self.direction
    
    def print_path(self) -> str:
        return self.print_map({'>': self.path[0], 'v': self.path[1], '<': self.path[2], '^': self.path[3], ' ': self.features[OPEN]})


def parse_path(input: str) -> list[int | str]:
    path: list[int | str] = []
    i = 0
    while i < len(input):
        if match := PATH_TILES.match(input, i):
            tiles_input = match.group()
            i += len(tiles_input)
            path.append(int(tiles_input))
        elif match := PATH_TURN.match(input, i):
            turn_input = match.group()
            i += len(turn_input)
            path.append(turn_input)
    return path
