from enum import IntEnum
import heapq
from typing import NamedTuple

from aoc.map import EmptyMap, Coordinate


class RegionType(IntEnum):
    ROCKY = 0
    WET = 1
    NARROW = 2


class Tools(IntEnum):
    NEITHER = 0
    TORCH = 1
    CLIMBING_GEAR = 2

    def compatible(self, region_type: RegionType) -> bool:
        match region_type:
            case RegionType.ROCKY:
                return self != Tools.NEITHER
            case RegionType.WET:
                return self != Tools.TORCH
            case RegionType.NARROW:
                return self != Tools.CLIMBING_GEAR


class Path(NamedTuple):
    heuristic: int
    length: int
    location: Coordinate
    tool: Tools


class CaveMap(EmptyMap):
    def __init__(self, depth: int, target: Coordinate):
        super().__init__(0, 0, target.x*7, target.y*7)
        self.depth = depth
        self.target = target
        self.erosion_levels: dict[Coordinate, int] = {Coordinate(0, 0): 0, target: 0}
    
    def geologic_index(self, location: Coordinate) -> int:
        if location.y == 0:
            return location.x * 16807
        if location.x == 0:
            return location.y * 48271
        return self.erosion_level(location._replace(x=location.x - 1)) * self.erosion_level(location._replace(y=location.y - 1))

    def erosion_level(self, location: Coordinate) -> int:
        if location not in self.erosion_levels:
            self.erosion_levels[location] = (self.geologic_index(location) + self.depth) % 20183
        return self.erosion_levels[location]
    
    def region_type(self, location: Coordinate) -> RegionType:
        return RegionType(self.erosion_level(location) % 3)
    
    def heuristic(self, length: int, location: Coordinate, tool: Tools) -> int:
        """A* heuristic for prioritizing path finding: manhattan distance plus tool change."""
        return length + location.difference(self.target).manhattan_distance() + (7 if tool != Tools.TORCH else 0)

    def new_path(self, length: int, location: Coordinate, tool: Tools) -> Path:
        return Path(self.heuristic(length, location, tool), length, location, tool)

    def next_cave_routes(self, path: Path) -> list['Path']:
        next_paths: list[Path] = []
        for neighbor in self.neighbors(path.location):
            if path.tool.compatible(self.region_type(neighbor)):
                next_paths.append(self.new_path(path.length + 1, neighbor, path.tool))
        for tool in Tools:
            if tool != path.tool and tool.compatible(self.region_type(path.location)):
                next_paths.append(self.new_path(path.length + 7, path.location, tool))
        return next_paths

    def shortest_cave_route(self) -> Path:
        visited: set[tuple[Coordinate, Tools]] = set()
        paths_to_try: list[Path] = []
        heapq.heappush(paths_to_try, self.new_path(0, Coordinate(0, 0), Tools.TORCH))

        while paths_to_try:
            path = heapq.heappop(paths_to_try)
            if (path.location, path.tool) in visited:
                continue
            visited.add((path.location, path.tool))

            if path.location == self.target and path.tool == Tools.TORCH:
                # Can only visit the ending location once, so the first time is the shortest path.
                return path

            for next_path in self.next_cave_routes(path):
                heapq.heappush(paths_to_try, next_path)

        raise ValueError(f'Failed to find a route through the cave.')
