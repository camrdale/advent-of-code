from collections import defaultdict
from typing import NamedTuple
from queue import PriorityQueue


class Offset(NamedTuple):
    """A delta between two Coordinates."""
    x: int
    y: int

    def negate(self) -> 'Offset':
        return Offset(-self.x, -self.y)


NEIGHBORS = [Offset(0, -1), Offset(1, 0), Offset(0, 1), Offset(-1, 0)]


class Coordinate(NamedTuple):
    x: int
    y: int

    def difference(self, other: 'Coordinate') -> Offset:
        return Offset(self.x - other.x, self.y - other.y)

    def add(self, offset: Offset) -> 'Coordinate':
        return Coordinate(self.x + offset.x, self.y + offset.y)
    
    def valid(self, width: int, height: int) -> bool:
        return 0 <= self.x < width and 0 <= self.y < height
    
    def neighbors(self) -> list['Coordinate']:
        return [self.add(offset) for offset in NEIGHBORS]


class Path(NamedTuple):
    length: int
    location: Coordinate
    previous: frozenset[Coordinate]

    def next_paths(self) -> list['Path']:
        new_previous = self.previous.union((self.location,))
        return [Path(self.length + 1, neighbor, new_previous)
                for neighbor in self.location.neighbors()
                if neighbor not in self.previous]


class EmptyMap:
    def __init__(self, width: int, height: int):
        self.height = height
        self.width = width
        self.save_features = ''
        self.features: dict[str, set[Coordinate]] = defaultdict(set)

    def valid(self, coordinate: Coordinate) -> bool:
        """Check if a Coordinate is valid for this map."""
        return coordinate.valid(self.width, self.height)

    def shortest_paths(
            self, 
            starting_pos: Coordinate, 
            ending_pos: Coordinate, 
            features_to_avoid: str
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

            for next_path in path.next_paths():
                if self.valid(next_path.location) and next_path.location not in coords_to_avoid:
                    paths_to_try.put(next_path)

        return visited, shortest_path

    def print_map(
            self, 
            additional_features: dict[str, set[Coordinate]] | None = None, 
            additional_feature_priority: bool = True) -> str:
        if additional_features is None:
            additional_features = {}
        s = ''
        for y in range(self.height):
            for x in range(self.width):
                s += self.print_coordinate(Coordinate(x,y), additional_features, additional_feature_priority)
            s += '\n'
        return s
    
    def print_coordinate(
            self, 
            c: Coordinate, 
            additional_features: dict[str, set[Coordinate]],
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


class ParsedMap(EmptyMap):
    def __init__(self, lines: list[str], save_features: str):
        """Construct a map from the 2D-array in lines, saving the Coordinates of any characters in save_features."""
        super().__init__(len(lines[0]), len(lines))
        self.save_features = save_features
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c in save_features:
                    self.features[c].add(Coordinate(x,y))
