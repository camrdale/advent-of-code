from collections import defaultdict
import collections.abc
from enum import IntEnum
from typing import NamedTuple, Self
from queue import PriorityQueue


class Offset(NamedTuple):
    """A delta between two Coordinates."""
    x: int
    y: int

    def negate(self) -> 'Offset':
        return Offset(-self.x, -self.y)

    def add(self, other: 'Offset') -> 'Offset':
        return Offset(self.x + other.x, self.y + other.y)
    
    def manhattan_distance(self) -> int:
        return abs(self.x) + abs(self.y)


UP = Offset(0, -1)
DOWN = Offset(0, 1)
LEFT = Offset(-1, 0)
RIGHT = Offset(1, 0)

NEIGHBORS = [UP, RIGHT, DOWN, LEFT]
DIAGONAL_NEIGHBORS = [Offset(-1, -1), Offset(1, -1), Offset(1, 1), Offset(-1, 1)]


class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def right(self) -> 'Direction':
        return Direction((self.value + 1) % 4)

    def left(self) -> 'Direction':
        return Direction((self.value - 1) % 4)
    
    def offset(self, _directions: dict[int, Offset] ={
            NORTH: Offset(0, -1),
            EAST: Offset(1, 0),
            SOUTH: Offset(0, 1),
            WEST: Offset(-1, 0)}) -> Offset:
        return _directions[self.value]

    @classmethod
    def from_offset(cls, offset: Offset, _offsets: dict[Offset, int] = {
            Offset(0, -1): NORTH,
            Offset(1, 0): EAST,
            Offset(0, 1): SOUTH,
            Offset(-1, 0): WEST}) -> Self:
        return cls(_offsets[offset])


class Coordinate(NamedTuple):
    x: int
    y: int

    def difference(self, from_coordinate: 'Coordinate') -> Offset:
        return Offset(self.x - from_coordinate.x, self.y - from_coordinate.y)

    def direction(self,  from_coordinate: 'Coordinate') -> Direction:
        return Direction.from_offset(self.difference(from_coordinate))
    
    def add(self, offset: Offset) -> 'Coordinate':
        return Coordinate(self.x + offset.x, self.y + offset.y)
    
    def valid(self, width: int, height: int) -> bool:
        return 0 <= self.x < width and 0 <= self.y < height
    
    def neighbors(self) -> list['Coordinate']:
        return [self.add(offset) for offset in NEIGHBORS]

    def diagonal_neighbors(self) -> list['Coordinate']:
        return [self.add(offset) for offset in DIAGONAL_NEIGHBORS]


class Offset3D(NamedTuple):
    z: int
    offset: Offset

    @classmethod
    def from_text(cls, text: str) -> 'Offset3D':
        x,y,z = list(map(int, text.split(',')))
        return cls(z, Offset(x,y))
    
    def negate(self) -> 'Offset3D':
        return Offset3D(-self.z, self.offset.negate())
    
    def add(self, offset: 'Offset3D') -> 'Offset3D':
        return Offset3D(self.z + offset.z, self.offset.add(offset.offset))


class Coordinate3D(NamedTuple):
    z: int  # First so sorting by z works.
    location: Coordinate

    @classmethod
    def from_text(cls, text: str) -> 'Coordinate3D':
        x,y,z = list(map(int, text.split(',')))
        return cls(z, Coordinate(x,y))
    
    def add(self, offset: Offset3D) -> 'Coordinate3D':
        return Coordinate3D(self.z + offset.z, self.location.add(offset.offset))
    
    def __str__(self) -> str:
        return f'(z={self.z},x={self.location.x},y={self.location.y})'


class Path(NamedTuple):
    length: int
    location: Coordinate
    previous: frozenset[Coordinate]

    def next_paths(self) -> list['Path']:
        new_previous = self.previous.union((self.location,))
        return [Path(self.length + 1, neighbor, new_previous)
                for neighbor in self.location.neighbors()
                if neighbor not in self.previous]


class UnknownMap:
    def __init__(self, save_features: str = ''):
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0
        self.save_features = save_features
        self.features: dict[str, set[Coordinate]] = defaultdict(set)
    
    def expand_map(self, location:Coordinate) -> None:
        if location.x < self.min_x:
            self.min_x = location.x
        if location.x > self.max_x:
            self.max_x = location.x
        if location.y < self.min_y:
            self.min_y = location.y
        if location.y > self.max_y:
            self.max_y = location.y

    def add_feature(self, feature: str, location: Coordinate) -> None:
        self.features[feature].add(location)
        self.expand_map(location)
    
    def valid(self, coordinate: Coordinate) -> bool:
        """Check if a Coordinate is valid for this map."""
        return self.min_x <= coordinate.x <= self.max_x and self.min_y <= coordinate.y <= self.max_y
    
    def at_location(self, coordinate: Coordinate) -> str:
        for feature, coords in self.features.items():
            if coordinate in coords:
                return feature
        return ''
    
    def neighbors(self, location: Coordinate) -> list['Coordinate']:
        return [neighbor for neighbor in location.neighbors() if self.valid(neighbor)]

    def next_paths(self, path: Path, coords_to_avoid: set[Coordinate]) -> list['Path']:
        new_previous = path.previous.union((path.location,))
        return [Path(path.length + 1, neighbor, new_previous)
                for neighbor in self.neighbors(path.location)
                if neighbor not in path.previous and neighbor not in coords_to_avoid]

    def shortest_paths(
            self, 
            starting_pos: Coordinate, 
            ending_pos: Coordinate, 
            features_to_avoid: str = ''
            ) -> tuple[dict[Coordinate, int], Path | None]:
        """Find the shortest paths from starting_pos, avoiding the features.
        
        Returns a dictionary containing all reachable Coordinates from
        starting_pos, with values of the shortest length of a path.
        Also returns a Path for a shortest path from starting_pos to
        ending_pos.
        """
        visited: dict[Coordinate, int] = {}
        shortest_path: Path | None = None
        paths_to_try: PriorityQueue[Path] = PriorityQueue()
        paths_to_try.put(Path(0, starting_pos, frozenset()))
        coords_to_avoid: set[Coordinate] = set().union(*(
            feature_set for feature, feature_set in self.features.items()
            if feature in features_to_avoid))

        while not paths_to_try.empty():
            path = paths_to_try.get()
            if path.location in visited:
                continue
            visited[path.location] = path.length

            if path.location == ending_pos:
                # Can only visit the ending location once, so the first time is the shortest path.
                shortest_path = path
                continue

            for next_path in self.next_paths(path, coords_to_avoid):
                paths_to_try.put(next_path)

        return visited, shortest_path

    def print_map(
            self, 
            additional_features: collections.abc.Mapping[str, collections.abc.Set[Coordinate]] | None = None, 
            additional_feature_priority: bool = True) -> str:
        if additional_features is None:
            additional_features = {}
        s = ''
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                s += self.print_coordinate(Coordinate(x,y), additional_features, additional_feature_priority)
            s += '\n'
        return s
    
    def print_coordinate(
            self, 
            c: Coordinate, 
            additional_features: collections.abc.Mapping[str, collections.abc.Set[Coordinate]],
            additional_feature_priority: bool) -> str:
        if additional_feature_priority:
            for feature, coords in additional_features.items():
                if c in coords:
                    return feature
        for feature in self.save_features:
            if c in self.features[feature]:
                return feature
        if not additional_feature_priority:
            for feature, coords in additional_features.items():
                if c in coords:
                    return feature
        return '.'


class EmptyMap(UnknownMap):
    def __init__(self, min_x: int, min_y: int, max_x: int, max_y: int, save_features: str = ''):
        super().__init__(save_features=save_features)
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y


class ParsedMap(UnknownMap):
    def __init__(self, lines: list[str], save_features: str):
        """Construct a map from the 2D-array in lines, saving the Coordinates of any characters in save_features."""
        super().__init__(save_features=save_features)
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c in save_features:
                    self.add_feature(c, Coordinate(x,y))
                else:
                    self.expand_map(Coordinate(x,y))
