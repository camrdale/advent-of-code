from typing import NamedTuple
from queue import PriorityQueue

from aoc import log
from aoc.map import Coordinate, Direction, ParsedMap

WALL = '#'
STARTING = 'S'
END = 'E'


class Situation(NamedTuple):
    location: Coordinate
    direction: Direction

    def forward(self) -> 'Situation':
        forward_location = self.location.add(self.direction.offset())
        return Situation(forward_location, self.direction)
    
    def clockwise(self) -> 'Situation':
        clockwise_direction = self.direction.right()
        return Situation(self.location.add(clockwise_direction.offset()), clockwise_direction)
    
    def counterclockwise(self) -> 'Situation':
        counterclockwise_direction = self.direction.left()
        return Situation(self.location.add(counterclockwise_direction.offset()), counterclockwise_direction)


class ReindeerPath(NamedTuple):
    score: int
    situation: Situation
    previous: tuple[Coordinate, ...] = ()

    def forward(self) -> 'ReindeerPath':
        return ReindeerPath(self.score + 1, self.situation.forward(), self.previous + (self.situation.location,))
    
    def clockwise(self) -> 'ReindeerPath':
        return ReindeerPath(self.score + 1001, self.situation.clockwise(), self.previous + (self.situation.location,))
    
    def counterclockwise(self) -> 'ReindeerPath':
        return ReindeerPath(self.score + 1001, self.situation.counterclockwise(), self.previous + (self.situation.location,))
    
    def next_paths(self) -> tuple['ReindeerPath', 'ReindeerPath', 'ReindeerPath']:
        return (self.forward(), self.clockwise(), self.counterclockwise())


class ReindeerMaze(ParsedMap):
    def __init__(self, lines: list[str]):
        super().__init__(lines, WALL + STARTING + END)
        self.walls: set[Coordinate] = self.features[WALL]
        (self.starting_pos,) = self.features[STARTING]
        (self.end_pos,) = self.features[END]
        self.starting_direction = Direction.EAST

    def lowest_score_paths(self, progress_bar: log.ProgressBar|None = None) -> list[ReindeerPath]:
        visited: dict[Situation, int] = {}
        paths_to_try: PriorityQueue[ReindeerPath] = PriorityQueue()
        found_paths: list[ReindeerPath] = []

        starting_situation = Situation(self.starting_pos, self.starting_direction)
        paths_to_try.put(ReindeerPath(0, starting_situation))

        while not paths_to_try.empty():
            path = paths_to_try.get()
            if progress_bar:
                progress_bar.update()
            if len(found_paths) > 0 and path.score > found_paths[0].score:
                return found_paths
            if path.situation.location == self.end_pos:
                found_paths.append(path)
                continue
            if path.situation in visited and path.score > visited[path.situation]:
                continue
            visited[path.situation] = path.score

            for next_path in path.next_paths():
                if next_path.situation.location not in self.walls:
                    paths_to_try.put(next_path)

        return found_paths
    
    def print_paths(self, paths: list[ReindeerPath]) -> str:
        visited: set[Coordinate] = set()
        for path in paths:
            visited.update(path.previous)
        return self.print_map({'O': visited}, additional_feature_priority=False)
