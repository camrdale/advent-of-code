import collections
from queue import PriorityQueue
import string
from typing import NamedTuple

from aoc.map import ParsedMap, Coordinate, Path

PORTAL_NAMES = string.ascii_letters + string.digits


def preprocess(input: list[str]) -> list[str]:
    """Replace 2-letter portal names adjacent to portal, with 1-letter portal name on the portal."""
    list_input = [list(line) for line in input]
    portals: dict[str, str] = {'AA' : 'A', 'ZZ': 'Z'}
    available_names = [c for c in PORTAL_NAMES if c not in portals.values()]
    for y in range(len(list_input)):
        for x in range(len(list_input[y])):
            if list_input[y][x] in string.ascii_uppercase:
                if x > 0 and list_input[y][x-1] in string.ascii_uppercase and x < len(list_input[y]) - 1 and list_input[y][x+1] == '.':
                    portal = list_input[y][x-1] + list_input[y][x]
                    if portal not in portals:
                        portals[portal] = available_names.pop(0)
                    list_input[y][x+1] = portals[portal]
                    list_input[y][x-1] = ' '
                    list_input[y][x] = ' '
                elif x > 0 and list_input[y][x-1] == '.' and x < len(list_input[y]) - 1 and list_input[y][x+1] in string.ascii_uppercase:
                    portal = list_input[y][x] + list_input[y][x+1]
                    if portal not in portals:
                        portals[portal] = available_names.pop(0)
                    list_input[y][x-1] = portals[portal]
                    list_input[y][x+1] = ' '
                    list_input[y][x] = ' '
                elif y > 0 and list_input[y-1][x] in string.ascii_uppercase and y < len(list_input) - 1 and list_input[y+1][x] == '.':
                    portal = list_input[y-1][x] + list_input[y][x]
                    if portal not in portals:
                        portals[portal] = available_names.pop(0)
                    list_input[y+1][x] = portals[portal]
                    list_input[y-1][x] = ' '
                    list_input[y][x] = ' '
                elif y > 0 and list_input[y-1][x] == '.' and y < len(list_input) - 1 and list_input[y+1][x] in string.ascii_uppercase:
                    portal = list_input[y][x] + list_input[y+1][x]
                    if portal not in portals:
                        portals[portal] = available_names.pop(0)
                    list_input[y-1][x] = portals[portal]
                    list_input[y+1][x] = ' '
                    list_input[y][x] = ' '
    return [''.join(line) for line in list_input]


class LevelLocation(NamedTuple):
    location: Coordinate
    level: int

    def neighbors(self) -> list['LevelLocation']:
        return [LevelLocation(neighbor, self.level) for neighbor in self.location.neighbors()]


class LevelPath(NamedTuple):
    length: int
    location: LevelLocation
    previous: frozenset[LevelLocation]


class PlutoMap(ParsedMap):
    def __init__(self, input: list[str]):
        super().__init__(preprocess(input), PORTAL_NAMES + '# ')
        self.portals: dict[str, list[Coordinate]] = collections.defaultdict(list)
        self.portal_locations: dict[Coordinate, str] = {}
        for portal in PORTAL_NAMES:
            for location in self.features[portal]:
                self.portal_locations[location] = portal
                self.portals[portal].append(location)

    def travel_through_portal(self, portal_location: Coordinate) -> Coordinate:
        portal = self.portal_locations[portal_location]
        portal_destinations = self.portals[portal]
        if len(portal_destinations) == 2:
            return [
                destination for destination in portal_destinations
                if destination != portal_location][0]
        raise ValueError(f'Cant travel through portal: {portal_location}')
    
    def precalculate_portal_paths(self) -> dict[Coordinate, dict[Coordinate, int]]:
        portal_paths: dict[Coordinate, dict[Coordinate, int]] = {}
        for location in self.portal_locations:
            visited = self.shortest_paths(location, Coordinate(-1,-1), '# ')[0]
            portal_paths[location] = dict(
                (next_location, distance)
                for next_location, distance in visited.items()
                if next_location in self.portal_locations and next_location != location
            )
        return portal_paths

    def shortest_path(
            self, 
            starting_pos: Coordinate, 
            ending_pos: Coordinate
            ) -> Path:
        portal_paths = self.precalculate_portal_paths()
        visited: dict[Coordinate, int] = {}
        paths_to_try: PriorityQueue[Path] = PriorityQueue()
        paths_to_try.put(Path(0, starting_pos, frozenset()))

        while not paths_to_try.empty():
            path = paths_to_try.get()
            if path.location in visited:
                continue
            visited[path.location] = path.length
            if path.location == ending_pos:
                return path

            for next_location, distance in portal_paths[path.location].items():
                if next_location == ending_pos:
                    paths_to_try.put(Path(
                        path.length + distance,
                        next_location,
                        path.previous.union(frozenset([path.location]))))
                
                if len(self.portals[self.portal_locations[next_location]]) == 2:
                    paths_to_try.put(Path(
                        path.length + distance + 1,
                        self.travel_through_portal(next_location),
                        path.previous.union(frozenset([path.location]))))

        raise ValueError(f'Failed to find a path from {starting_pos} to {ending_pos}')

    def outer_portal(self, location: Coordinate) -> bool:
        return (
            location.x == self.min_x + 2 or 
            location.x == self.max_x - 2 or 
            location.y == self.min_y + 2 or 
            location.y == self.max_y - 2
        )
    
    def level_neighbors(self, location: LevelLocation, coords_to_avoid: set[Coordinate]) -> list['LevelLocation']:
        neighbors = [
            neighbor
            for neighbor in location.neighbors()
            if self.valid(neighbor.location) and neighbor.location not in coords_to_avoid]
        if location.location in self.portal_locations:
            portal = self.portal_locations[location.location]
            portal_destinations = self.portals[portal]
            if len(portal_destinations) == 2:
                neighbor = [destination for destination in portal_destinations if destination != location.location][0]
                outer_portal = self.outer_portal(location.location)
                if not outer_portal or location.level != 0:
                    neighbors.append(LevelLocation(neighbor, location.level + (-1 if outer_portal else 1)))
        return neighbors

    def next_level_paths(
            self, 
            path: LevelPath, 
            outermost_coords_to_avoid: set[Coordinate], 
            inner_coords_to_avoid: set[Coordinate]
            ) -> list['LevelPath']:
        new_previous = path.previous.union((path.location,))
        coords_to_avoid = outermost_coords_to_avoid if path.location.level == 0 else inner_coords_to_avoid
        return [LevelPath(path.length + 1, neighbor, new_previous)
                for neighbor in self.level_neighbors(path.location, coords_to_avoid)
                if neighbor not in path.previous]

    def shortest_level_path(
            self, 
            starting_pos: LevelLocation, 
            ending_pos: LevelLocation
            ) -> LevelPath:
        portal_paths = self.precalculate_portal_paths()
        visited: dict[LevelLocation, int] = {}
        paths_to_try: PriorityQueue[LevelPath] = PriorityQueue()
        paths_to_try.put(LevelPath(0, starting_pos, frozenset()))

        while not paths_to_try.empty():
            path = paths_to_try.get()
            if path.location in visited:
                continue
            visited[path.location] = path.length
            if path.location == ending_pos:
                return path

            for next_location, distance in portal_paths[path.location.location].items():
                if next_location == ending_pos.location and path.location.level == ending_pos.level:
                    paths_to_try.put(LevelPath(
                        path.length + distance,
                        ending_pos,
                        path.previous.union(frozenset([path.location]))))
                if path.location.level == 0 and self.outer_portal(next_location):
                    continue
                if len(self.portals[self.portal_locations[next_location]]) == 2:
                    paths_to_try.put(LevelPath(
                        path.length + distance + 1,
                        LevelLocation(
                            self.travel_through_portal(next_location),
                            path.location.level + (-1 if self.outer_portal(next_location) else 1)),
                        path.previous.union(frozenset([path.location]))))
                    
        raise ValueError(f'Failed to find a path from {starting_pos} to {ending_pos}')
