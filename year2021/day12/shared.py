from typing import Any, NamedTuple

import cachetools

MAX_CACHE_SIZE = 20000000


class Cave:
    def __init__(self, name: str):
        self.name = name
        self.neighbors: list[Cave] = []

    def small(self) -> bool:
        return self.name.islower()
    
    def add_neighbor(self, neighbor: 'Cave') -> None:
        self.neighbors.append(neighbor)

    def __eq__(self, other: Any) -> bool:
        if type(other) != Cave:
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
    
    def __repr__(self) -> str:
        return self.name


class CavePath(NamedTuple):
    location: Cave
    previous: frozenset[Cave]
    small_cave_twice: bool

    def next_paths(self) -> list['CavePath']:
        new_previous = self.previous.union((self.location,))
        next_paths = [
            CavePath(neighbor, new_previous, self.small_cave_twice)
            for neighbor in self.location.neighbors
            if not neighbor.small() or neighbor not in self.previous]
        if not self.small_cave_twice:
            next_paths.extend([
                CavePath(neighbor, new_previous, True)
                for neighbor in self.location.neighbors
                if neighbor.small() and neighbor in self.previous and neighbor.name not in ('start', 'end')
            ])
        return next_paths


class CaveMap:
    def __init__(self, input: list[str]):
        self.caves: dict[str, Cave] = {}
        for line in input:
            name_a, name_b = line.split('-')
            self.add_connection(self.get_cave(name_a), self.get_cave(name_b))
        self.cache: cachetools.LRUCache[tuple[str], int] = cachetools.LRUCache(maxsize=MAX_CACHE_SIZE)

    def get_cave(self, name: str) -> Cave:
        if name in self.caves:
            return self.caves[name]

        cave = Cave(name)
        self.caves[name] = cave
        return cave

    def add_connection(self, cave_a: Cave, cave_b: Cave):
        cave_a.add_neighbor(cave_b)
        cave_b.add_neighbor(cave_a)

    @cachetools.cachedmethod(lambda self: self.cache)
    def _cached_num_paths(self, starting_path: CavePath, ending: str) -> int:
        if starting_path.location.name == ending:
            return 1
        return sum(self._cached_num_paths(next_path, ending) for next_path in starting_path.next_paths())

    def num_paths(
            self,
            starting: str,
            ending: str,
            one_small_cave_twice: bool = False
            ) -> int:
        return self._cached_num_paths(CavePath(self.caves[starting], frozenset(), not one_small_cave_twice), ending)
