import collections
import queue
import string
from typing import NamedTuple

import cachetools

from aoc.map import ParsedMap, Coordinate

MAX_CACHE_SIZE = 2000000


class Visit(NamedTuple):
    keys_required: frozenset[str]
    length: int


class Path(NamedTuple):
    length: int
    location: Coordinate
    keys_required: frozenset[str]


class VisitedSet:
    def __init__(self):
        self.visited: dict[Coordinate, list[Visit]] = collections.defaultdict(list)

    def already_visited(self, path: Path) -> bool:
        for visit in self.visited[path.location]:
            if visit.keys_required <= path.keys_required:
                return True
        self.visited[path.location].append(Visit(frozenset(path.keys_required), path.length))
        return False

    def keep_locations(self, locations: set[Coordinate]) -> None:
        for location in list(self.visited.keys()):
            if location not in locations:
                del self.visited[location]
    
    def possible_locations(self, keys_acquired: frozenset[str]) -> dict[Coordinate, int]:
        result: dict[Coordinate, int] = {}
        for location, visits in self.visited.items():
            for visit in visits:
                if visit.keys_required <= keys_acquired:
                    if location not in result or result[location] > visit.length:
                        result[location] = visit.length
        return result

    def __repr__(self) -> str:
        return str(self.visited)


class VaultMap(ParsedMap):
    def __init__(self, input: list[str]):
        super().__init__(input, string.ascii_letters + '@#')
        self.entrances: tuple[Coordinate, ...] = next(iter(self.features['@'])),

        self.keys: dict[str, Coordinate] = {}
        self.key_locations: dict[Coordinate, str] = {}
        for key in string.ascii_lowercase:
            if key in self.features:
                location = next(iter(self.features[key]))
                self.keys[key] = location
                self.key_locations[location] = key
        self.locks: dict[str, Coordinate] = {}
        for lock in string.ascii_uppercase:
            if lock in self.features:
                self.locks[lock] = next(iter(self.features[lock]))
        self.cache: cachetools.LRUCache[tuple[str], int] = cachetools.LRUCache(maxsize=MAX_CACHE_SIZE)

    def build_visited_sets(self):
        self.visited_sets: dict[Coordinate, VisitedSet] = {}
        key_locations = set(self.key_locations.keys())
        for location in self.key_locations:
            visited_set = self.build_visited_set(location)
            visited_set.keep_locations(key_locations)
            self.visited_sets[location] = visited_set
        for entrance in self.entrances:
            self.visited_sets[entrance] = self.build_visited_set(entrance)
            self.visited_sets[entrance].keep_locations(key_locations)

    def build_visited_set(self, starting_location: Coordinate) -> VisitedSet:
        visited_set = VisitedSet()
        paths_to_try: queue.PriorityQueue[Path] = queue.PriorityQueue()
        paths_to_try.put(Path(0, starting_location, frozenset()))

        while not paths_to_try.empty():
            path = paths_to_try.get()
            if visited_set.already_visited(path):
                continue

            for neighbor in path.location.neighbors():
                if self.valid(neighbor) and neighbor not in self.features['#']:
                    keys_required = path.keys_required
                    at_location = self.at_location(neighbor)
                    if at_location and at_location in self.locks:
                        keys_required = keys_required.union([at_location.lower()])
                    paths_to_try.put(Path(path.length + 1, neighbor, keys_required))

        return visited_set
    
    @cachetools.cachedmethod(lambda self: self.cache)
    def shortest_key_path(
            self, 
            current_locations: tuple[Coordinate, ...], 
            keys_remaining: frozenset[str]
            ) -> int:
        if not keys_remaining:
            return 0

        current_keys = frozenset(self.keys.keys()) - keys_remaining
        shortest_path = 10000000000000
        for i, current_location in enumerate(current_locations):
            visited_set = self.visited_sets[current_location]
            for next_location, length in visited_set.possible_locations(current_keys).items():
                key = self.key_locations[next_location]
                if key not in keys_remaining:
                    continue
                next_locations = list(current_locations)
                next_locations[i] = next_location
                path_length = length + self.shortest_key_path(tuple(next_locations), keys_remaining - frozenset([key]))
                if path_length < shortest_path:
                    shortest_path = path_length

        return shortest_path
