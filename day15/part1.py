#!/usr/bin/python

from typing import NamedTuple
from collections.abc import Iterable
from pathlib import Path

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'
TEST_INPUT = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

WALL = '#'
BOX = 'O'

UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'


class Offset(NamedTuple):
    x: int
    y: int


DIRECTIONS = {
    UP: Offset(0, -1),
    RIGHT: Offset(1, 0),
    DOWN: Offset(0, 1),
    LEFT: Offset(-1, 0)}


class Coordinate(NamedTuple):
    x: int
    y: int
    
    def add(self, offset: Offset) -> 'Coordinate':
        return Coordinate(self.x + offset.x, self.y + offset.y)
    
    def valid(self, width: int, height: int) -> bool:
        return 0 <= self.x < width and 0 <= self.y < height


class WarehouseMap:
    def __init__(self, lines: Iterable[str]):
        self.locations: dict[Coordinate, str] = {}
        self.height = 0
        self.width = 0
        self.current_pos: Coordinate = Coordinate(-1,-1)
        for y, line in enumerate(lines):
            if len(line) > 0:
                self.width = len(line.strip())
                self.height += 1
                for x, c in enumerate(line.strip()):
                    if c in (WALL, BOX):
                        self.locations[Coordinate(x,y)] = c
                    elif c == '@':
                        self.current_pos = Coordinate(x,y)

    def move(self, direction: str):
        offset = DIRECTIONS[direction]
        target = self.current_pos.add(offset)
        
        target_contents = self.locations.get(target, None)
        if target_contents is None:
            self.current_pos = target
            return
        if target_contents == WALL:
            return
        
        end = target.add(offset)
        while self.locations.get(end, None) == BOX:
            end = end.add(offset)
        
        end_contents = self.locations.get(end, None)
        if end_contents == WALL:
            return
        self.locations[end] = BOX
        del self.locations[target]
        self.current_pos = target

    def sum_box_positions(self) -> int:
        return sum(pos.x + 100*pos.y for pos, contents in self.locations.items() if contents == BOX)


def main():
    map_input: list[str] = []
    move_input = ''
    with INPUT_FILE.open() as ifp:
        map_time = True
        # for line in TEST_INPUT.split('\n'):
        for line in ifp.readlines():
            if map_time:
                if line.strip() == '':
                    map_time = False
                else:
                    map_input.append(line.strip())
            else:
                move_input += line.strip()

    map = WarehouseMap(map_input)

    for direction in move_input:
        map.move(direction)

    print('Sum of box GPS coordinates:', map.sum_box_positions())


if __name__ == '__main__':
    main()
