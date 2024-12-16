#!/usr/bin/python

from enum import IntEnum
from typing import NamedTuple
from collections.abc import Iterable
from queue import PriorityQueue

WALL = '#'
STARTING = 'S'
END = 'E'


class Offset(NamedTuple):
    x: int
    y: int


class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def next(self) -> 'Direction':
        return Direction((self.value + 1) % 4)

    def prev(self) -> 'Direction':
        return Direction((self.value - 1) % 4)
    
    def offset(self, _directions: dict[int, Offset] ={
            NORTH: Offset(0, -1),
            EAST: Offset(1, 0),
            SOUTH: Offset(0, 1),
            WEST: Offset(-1, 0)}) -> Offset:
        return _directions[self.value]


class Coordinate(NamedTuple):
    x: int
    y: int

    def add(self, offset: Offset) -> 'Coordinate':
        return Coordinate(self.x + offset.x, self.y + offset.y)
    
    def valid(self, width: int, height: int) -> bool:
        return 0 <= self.x < width and 0 <= self.y < height
    

class Situation(NamedTuple):
    location: Coordinate
    direction: Direction

    def forward(self) -> 'Situation':
        forward_location = self.location.add(self.direction.offset())
        return Situation(forward_location, self.direction)
    
    def clockwise(self) -> 'Situation':
        clockwise_direction = self.direction.next()
        return Situation(self.location.add(clockwise_direction.offset()), clockwise_direction)
    
    def counterclockwise(self) -> 'Situation':
        counterclockwise_direction = self.direction.prev()
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


class ReindeerMaze:
    def __init__(self, lines: Iterable[str]):
        self.walls: set[Coordinate] = set()
        self.height = 0
        self.width = 0
        self.starting_pos: Coordinate = Coordinate(-1,-1)
        self.end_pos: Coordinate = Coordinate(-1,-1)
        self.starting_direction = Direction.EAST
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

    def lowest_score_paths(self) -> list[ReindeerPath]:
        visited: dict[Situation, int] = {}
        paths_to_try: PriorityQueue[ReindeerPath] = PriorityQueue()
        found_paths: list[ReindeerPath] = []

        starting_situation = Situation(self.starting_pos, self.starting_direction)
        paths_to_try.put(ReindeerPath(0, starting_situation))

        while not paths_to_try.empty():
            path = paths_to_try.get()
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
        s = ''
        visited: set[Coordinate] = set()
        for path in paths:
            visited.update(path.previous)
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
