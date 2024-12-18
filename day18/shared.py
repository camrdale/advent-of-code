#!/usr/bin/python

from collections.abc import Iterable
from typing import NamedTuple
from queue import PriorityQueue


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
    

class ReindeerPath(NamedTuple):
    score: int
    location: Coordinate
    previous: frozenset[Coordinate]

    def next_paths(self) -> list['ReindeerPath']:
        new_previous = self.previous.union((self.location,))
        return [ReindeerPath(self.score + 1, neighbor, new_previous)
                for neighbor in self.location.neighbors()
                if neighbor not in self.previous]


class ReindeerMaze:
    def __init__(self, width: int, height: int):
        self.walls: set[Coordinate] = set()
        self.height = height
        self.width = width
        self.starting_pos: Coordinate = Coordinate(0,0)
        self.end_pos: Coordinate = Coordinate(width-1,height-1)
        for y in range(-1, height+1):
            self.walls.add(Coordinate(-1,y))
            self.walls.add(Coordinate(width,y))
        for x in range(-1, width+1):
            self.walls.add(Coordinate(x,-1))
            self.walls.add(Coordinate(x,height))

    def add_walls(self, new_walls: Iterable[Coordinate]) -> None:
        self.walls.update(new_walls)

    def lowest_score_path(self) -> ReindeerPath | None:
        visited: dict[Coordinate, int] = {}
        paths_to_try: PriorityQueue[ReindeerPath] = PriorityQueue()
        paths_to_try.put(ReindeerPath(0, self.starting_pos, frozenset()))

        while not paths_to_try.empty():
            path = paths_to_try.get()
            if path.location == self.end_pos:
                return path
            if path.location in visited:
                continue
            visited[path.location] = path.score

            for next_path in path.next_paths():
                if next_path.location not in self.walls:
                    paths_to_try.put(next_path)

        return None
    
    def print_path(self, path: ReindeerPath) -> str:
        s = ''
        visited: set[Coordinate] = set(path.previous)
        for y in range(-1, self.height+1):
            for x in range(-1, self.width+1):
                c = Coordinate(x,y)
                if c in self.walls:
                    s += '#'
                elif c == self.starting_pos:
                    s += 'S'
                elif c == self.end_pos:
                    s += 'E'
                elif c in visited:
                    s += 'O'
                else:
                    s += '.'
            s += '\n'
        return s
