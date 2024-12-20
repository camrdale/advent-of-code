from collections import defaultdict
from collections.abc import Iterable
from typing import NamedTuple
from queue import PriorityQueue

WALL = '#'
STARTING = 'S'
END = 'E'


class Offset(NamedTuple):
    x: int
    y: int


NEIGHBORS = [Offset(1,0), Offset(0,1), Offset(-1,0), Offset(0,-1)]


class Coordinate(NamedTuple):
    x: int
    y: int

    def add(self, offset: Offset) -> 'Coordinate':
        return Coordinate(self.x + offset.x, self.y + offset.y)
    
    def valid(self, width: int, height: int) -> bool:
        return 0 <= self.x < width and 0 <= self.y < height
    
    def neighbors(self) -> list['Coordinate']:
        return [self.add(offset) for offset in NEIGHBORS]
    

class ProgramPath(NamedTuple):
    score: int
    location: Coordinate
    previous: frozenset[Coordinate]

    def next_paths(self) -> list['ProgramPath']:
        new_previous = self.previous.union((self.location,))
        return [ProgramPath(self.score + 1, neighbor, new_previous)
                for neighbor in self.location.neighbors()
                if neighbor not in self.previous]


class Cheat(NamedTuple):
    start: Coordinate
    end: Coordinate


class Racetrack:
    def __init__(self, lines: Iterable[str]):
        self.walls: set[Coordinate] = set()
        self.height = 0
        self.width = 0
        self.starting_pos: Coordinate = Coordinate(-1,-1)
        self.end_pos: Coordinate = Coordinate(-1,-1)
        for y, line in enumerate(lines):
            if len(line.strip()) > 0:
                self.width = len(line.strip())
                self.height += 1
                for x, c in enumerate(line.strip()):
                    if c == WALL:
                        self.walls.add(Coordinate(x,y))
                    elif c == STARTING:
                        self.starting_pos = Coordinate(x,y)
                    elif c == END:
                        self.end_pos = Coordinate(x,y)

    def all_cheats(self, cheats_last: int) -> dict[int, set[Cheat]]:
        time_to_finish: dict[Coordinate, int] = {}
        paths_to_try: PriorityQueue[ProgramPath] = PriorityQueue()
        paths_to_try.put(ProgramPath(0, self.end_pos, frozenset()))

        while not paths_to_try.empty():
            path = paths_to_try.get()
            if path.location in time_to_finish:
                continue
            time_to_finish[path.location] = path.score

            if path.location == self.starting_pos:
                continue

            for next_path in path.next_paths():
                if next_path.location not in self.walls:
                    paths_to_try.put(next_path)

        cheats: dict[int, set[Cheat]] = defaultdict(set)

        for start_location, finishing_time in time_to_finish.items():
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
    
    def print_path(self, path: ProgramPath) -> str:
        s = ''
        visited: set[Coordinate] = set(path.previous)
        for y in range(self.height):
            for x in range(self.width):
                c = Coordinate(x,y)
                if c in self.walls:
                    s += WALL
                elif c == self.starting_pos:
                    s += STARTING
                elif c == self.end_pos:
                    s += END
                elif c in visited:
                    s += 'O'
                else:
                    s += '.'
            s += '\n'
        return s
