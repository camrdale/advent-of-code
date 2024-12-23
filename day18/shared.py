from collections.abc import Iterable

from aoc.map import Coordinate, Path, EmptyMap

WALL = '#'


class ReindeerMaze(EmptyMap):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.walls: set[Coordinate] = self.features[WALL]
        self.starting_pos: Coordinate = Coordinate(0,0)
        self.end_pos: Coordinate = Coordinate(width-1,height-1)

    def add_walls(self, new_walls: Iterable[Coordinate]) -> None:
        self.walls.update(new_walls)

    def shortest_path(self) -> Path | None:
        _, shortest_path = self.shortest_paths(self.starting_pos, self.end_pos, WALL)
        return shortest_path
    
    def print_path(self, path: Path) -> str:
        return self.print_map({'O': set(path.previous)}, additional_feature_priority=False)
