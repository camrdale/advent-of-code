from collections import defaultdict
from collections.abc import Iterable
from typing import NamedTuple

from aoc import log
from aoc.map import Coordinate, Offset, ParsedMap

WALL = '#'
STARTING = 'S'
END = 'E'


class Cheat(NamedTuple):
    start: Coordinate
    end: Coordinate


class Racetrack(ParsedMap):
    def __init__(self, lines: list[str]):
        super().__init__(lines, WALL + STARTING + END)
        self.walls: set[Coordinate] = self.features[WALL]
        (self.starting_pos,) = self.features[STARTING]
        (self.end_pos,) = self.features[END]

    def all_cheats(self, cheats_last: int) -> dict[int, set[Cheat]]:
        time_to_finish, _ = self.shortest_paths(self.end_pos, self.starting_pos, WALL)
        cheats: dict[int, set[Cheat]] = defaultdict(set)

        for start_location, finishing_time in log.progress_bar(time_to_finish.items(), desc='day 20'):
            for x_offset in range(-cheats_last, cheats_last + 1):
                for y_offset in range(-cheats_last + abs(x_offset), cheats_last - abs(x_offset) + 1):
                    offset = Offset(x_offset, y_offset)
                    end_location = start_location.add(offset)
                    if end_location not in time_to_finish:
                        continue
                    cheat_savings = finishing_time - time_to_finish[end_location] - abs(x_offset) - abs(y_offset)
                    if cheat_savings > 0:
                        cheats[cheat_savings].add(Cheat(start_location, end_location))

        return cheats
    
    def print_cheats(self, cheats: Iterable[Cheat]) -> str:
        features: dict[str, set[Coordinate]] = defaultdict(set)
        for cheat in cheats:
            features['1'].add(cheat.start)
            features['2'].add(cheat.end)

        return self.print_map(features)
