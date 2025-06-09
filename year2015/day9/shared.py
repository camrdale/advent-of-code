import re


DISTANCE = re.compile(r'(.*) to (.*) = ([0-9]*)')


class SantaPlan:
    def __init__(self, input: list[str]) -> None:
        self.locations: set[str] = set()
        self.distances: dict[frozenset[str], int] = {}
        for line in input:
            distance = DISTANCE.match(line)
            if distance is None:
                raise ValueError(f'Failed to parse: {line}')
            pair = frozenset(distance.groups()[:2])
            self.locations.update(pair)
            self.distances[pair] = int(distance.group(3))

    def _shortest_path(self, start: str, locations: frozenset[str]) -> int:
        if not locations:
            return 0
        return min(self.distances[frozenset([start, location])] + self._shortest_path(location, locations - {location})
                   for location in locations)
    
    def shortest_path(self) -> int:
        return min(self._shortest_path(location, frozenset(self.locations - {location}))
                   for location in self.locations)

    def _longest_path(self, start: str, locations: frozenset[str]) -> int:
        if not locations:
            return 0
        return max(self.distances[frozenset([start, location])] + self._longest_path(location, locations - {location})
                   for location in locations)
    
    def longest_path(self) -> int:
        return max(self._longest_path(location, frozenset(self.locations - {location}))
                   for location in self.locations)
