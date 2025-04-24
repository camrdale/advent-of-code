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
        self.all_locations = self.features[WALL].union(self.features[OPEN])

    def wrap(self, location: Coordinate, direction: int, new_location: Coordinate, new_direction: int):
        """Adds the edge mapping and the reverse."""
        assert location in self.all_locations
        assert new_location in self.all_locations
        self.wraps[location, direction] = new_location, new_direction
        self.wraps[new_location, (new_direction + 2) % 4] = location, ((direction + 2) % 4)

    def calculate_edge_wrapping(self):
        """Calculates edge mappings for simple wrapping."""
        min_x_for_row: dict[int, int] = defaultdict(lambda: self.max_x)
        max_x_for_row: dict[int, int] = defaultdict(int)
        min_y_for_column: dict[int, int] = defaultdict(lambda: self.max_y)
        max_y_for_column: dict[int, int] = defaultdict(int)
        for location in self.all_locations:
            min_x_for_row[location.y] = min(min_x_for_row[location.y], location.x)
            max_x_for_row[location.y] = max(max_x_for_row[location.y], location.x)
            min_y_for_column[location.x] = min(min_y_for_column[location.x], location.y)
            max_y_for_column[location.x] = max(max_y_for_column[location.x], location.y)
        for row in range(self.min_y, self.max_y + 1):
            self.wrap(Coordinate(max_x_for_row[row], row), 0, Coordinate(min_x_for_row[row], row), 0)
        for column in range(self.min_x, self.max_x + 1):
            self.wrap(Coordinate(column, max_y_for_column[column]), 1, Coordinate(column, min_y_for_column[column]), 1)

    def off_edge_direction(self, location: Coordinate, direction: int) -> int:
        """The direction to go to fall of the edge from a location."""
        if location.add(DIRECTIONS[(direction + 1) % 4]) not in self.all_locations:
            return (direction + 1) % 4
        elif location.add(DIRECTIONS[(direction - 1) % 4]) not in self.all_locations:
            return (direction - 1) % 4
        raise ValueError(f'{location} does not have an edge with direction {direction}')

    def traverse_edge(self, location: Coordinate, direction: int) -> tuple[Coordinate, Coordinate, int]:
        """Traverse an edge along a direction.
        
        Returns the last coordinate on the edge, the first coordinate on the
        next edge, and the direction of the next edge. For an outer corner,
        the two returned coordinates will be the same.
        """
        off_edge_direction = self.off_edge_direction(location, direction)

        next_location = location.add(DIRECTIONS[direction])
        while next_location in self.all_locations and next_location.add(DIRECTIONS[off_edge_direction]) not in self.all_locations:
            location = next_location
            next_location = location.add(DIRECTIONS[direction])

        if next_location in self.all_locations:
            # inner corner
            return location, next_location.add(DIRECTIONS[off_edge_direction]), off_edge_direction

        # outer corner
        return location, location, (off_edge_direction + 2) % 4

    def wrap_edges(self, edge_length: int, edge1_location: Coordinate, edge1_direction: int, edge2_location: Coordinate, edge2_direction: int):
        """Add all the wrappings for one pair of edges."""
        edge1_off_edge_direction = self.off_edge_direction(edge1_location, edge1_direction)
        edge2_on_edge_direction = (self.off_edge_direction(edge2_location, edge2_direction) + 2) % 4
        for _ in range(edge_length):
            self.wrap(edge1_location, edge1_off_edge_direction, edge2_location, edge2_on_edge_direction)
            edge1_location = edge1_location.add(DIRECTIONS[edge1_direction])
            edge2_location = edge2_location.add(DIRECTIONS[edge2_direction])

    def cube_wrappings_from_inner_corner(self, edge1_location: Coordinate, edge1_direction: int, edge2_location: Coordinate, edge2_direction: int):
        """Calculate the wrappings from an inner corner by traversing outwards in both directions."""
        # Determine the length of each of the edges and where they turn at the end.
        edge1_end_location, edge1_next_location, edge1_next_direction = self.traverse_edge(edge1_location, edge1_direction)
        edge2_end_location, edge2_next_location, edge2_next_direction = self.traverse_edge(edge2_location, edge2_direction)
        edge1_length = edge1_end_location.difference(edge1_location).manhattan_distance() + 1
        edge2_length = edge2_end_location.difference(edge2_location).manhattan_distance() + 1

        # The inner corner is fully wrapped when both directions we are traversing encounter a corner at the same time.
        while edge1_length != edge2_length:
            if edge1_length > edge2_length:
                self.wrap_edges(edge2_length, edge1_location, edge1_direction, edge2_location, edge2_direction)

                # Remove the portion of the longer edge that was wrapped.
                edge1_length -= edge2_length
                edge1_location = edge1_location.add(DIRECTIONS[edge1_direction].times(edge2_length))

                # Turn the corner and traverse the next edge of the one that ended.
                edge2_location, edge2_direction = edge2_next_location, edge2_next_direction
                edge2_end_location, edge2_next_location, edge2_next_direction = self.traverse_edge(edge2_location, edge2_direction)
                edge2_length = edge2_end_location.difference(edge2_location).manhattan_distance() + 1
            else:
                self.wrap_edges(edge1_length, edge1_location, edge1_direction, edge2_location, edge2_direction)

                # Remove the portion of the longer edge that was wrapped.
                edge2_length -= edge1_length
                edge2_location = edge2_location.add(DIRECTIONS[edge2_direction].times(edge1_length))

                # Turn the corner and traverse the next edge of the one that ended.
                edge1_location, edge1_direction = edge1_next_location, edge1_next_direction
                edge1_end_location, edge1_next_location, edge1_next_direction = self.traverse_edge(edge1_next_location, edge1_next_direction)
                edge1_length = edge1_end_location.difference(edge1_location).manhattan_distance() + 1

        self.wrap_edges(edge1_length, edge1_location, edge1_direction, edge2_location, edge2_direction)

    def calculate_cube_wrapping(self):
        """Calculates wrapping around a flattened cube."""
        starting_location = self.location
        starting_direction = self.direction

        # Find all the inner corners to calculate wrappings outward from.
        # Corners are identified by the two edge directions to traverse from them.
        inner_corners: list[tuple[tuple[Coordinate, int], tuple[Coordinate, int]]] = []

        last_location, next_location, next_direction = self.traverse_edge(starting_location, starting_direction)
        if last_location != next_location:
            inner_corners.append(((last_location, (starting_direction + 2) % 4), (next_location, next_direction)))

        while next_location != starting_location:
            old_direction = next_direction
            last_location, next_location, next_direction = self.traverse_edge(next_location, next_direction)
            if last_location != next_location:
                inner_corners.append(((last_location, (old_direction + 2) % 4), (next_location, next_direction)))

        for (edge1_location, edge1_direction), (edge2_location, edge2_direction) in inner_corners:
            log.log(log.DEBUG, f'Found an inner corner from edge {edge1_location}:{edge1_direction} to edge {edge2_location}:{edge2_direction}')
            self.cube_wrappings_from_inner_corner(edge1_location, edge1_direction, edge2_location, edge2_direction)

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
