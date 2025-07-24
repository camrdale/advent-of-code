import itertools
import string

from aoc import log
from aoc.map import ParsedMap


WALL = '#'
START = '0'


class AirDuctMap(ParsedMap):
    def __init__(self, lines: list[str]):
        super().__init__(lines, WALL + string.digits)
        self.starting_location = next(iter(self.features[START]))
        self.points_of_interest = {c: next(iter(self.features[c])) for c in string.digits if c in self.features}

    def location_travel(self) -> dict[tuple[str, str], int]:
        """Build a dict of travel times between all points of interest."""
        location_travel: dict[tuple[str, str], int] = {}
        for start_at, start_location in self.points_of_interest.items():
            visited, _ = self.shortest_paths(start_location, start_location, WALL)
            for other_location, location in self.points_of_interest.items():
                if other_location == start_at:
                    continue
                location_travel[(start_at, other_location)] = visited[location]
        return location_travel

    def all_locations_route(self) -> int:
        location_travel = self.location_travel()
        shortest_route = 1000000000
        for path in itertools.permutations([c for c in self.points_of_interest if c != START]):
            route = sum([
                location_travel[(path[i-1] if i-1 >= 0 else START, path[i])]
                for i in range(len(path))])
            if route < shortest_route:
                log.log(log.INFO, f'Found shorter route {route}: {path}')
                shortest_route = route

        return shortest_route

    def all_locations_and_back_route(self) -> int:
        location_travel = self.location_travel()
        shortest_route = 1000000000
        for path in itertools.permutations([c for c in self.points_of_interest if c != START]):
            route = sum([
                location_travel[(path[i-1] if i-1 >= 0 else START, path[i])]
                for i in range(len(path))])
            route += location_travel[(path[-1], START)]
            if route < shortest_route:
                log.log(log.INFO, f'Found shorter route {route}: {path}')
                shortest_route = route

        return shortest_route
