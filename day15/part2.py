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


class Box(NamedTuple):
    left: Coordinate

    def right(self) -> Coordinate:
        return self.left.add(DIRECTIONS[RIGHT])
    
    def occupies(self) -> tuple[Coordinate, Coordinate]:
        return (self.left, self.right())
    
    def targets(self, direction: str) -> tuple[Coordinate, ...]:
        """Returns the target coordinates that need to be free for a move in a direction."""
        offset = DIRECTIONS[direction]
        if direction in (UP, DOWN):
            return (self.left.add(offset), self.right().add(offset))
        elif direction == LEFT:
            return (self.left.add(offset),)
        else:
            return (self.right().add(offset),)


class WarehouseMap:
    def __init__(self, lines: Iterable[str]):
        self.locations: dict[Coordinate, str | Box] = {}
        self.height = 0
        self.width = 0
        self.current_pos: Coordinate = Coordinate(-1,-1)
        for y, line in enumerate(lines):
            if len(line) > 0:
                self.width = len(line.strip())*2
                self.height += 1
                for x, c in enumerate(line.strip()):
                    if c == BOX:
                        box = Box(Coordinate(2*x,y))
                        for location in box.occupies():
                            self.locations[location] = box
                    elif c == WALL:
                        self.locations[Coordinate(2*x,y)] = WALL
                        self.locations[Coordinate(2*x + 1,y)] = WALL
                    elif c == '@':
                        self.current_pos = Coordinate(2*x,y)

    def move_box(self, box: Box, direction: str) -> None:
        offset = DIRECTIONS[direction]
        targets = box.targets(direction)
        target_contents: set[str | Box] = set(
            self.locations[target] for target in targets if target in self.locations)
        for target_box in target_contents:
            assert(isinstance(target_box, Box))
            self.move_box(target_box, direction)
        for location in box.occupies():
            del self.locations[location]
        new_box = Box(box.left.add(offset))
        for location in new_box.occupies():
            self.locations[location] = new_box

    def can_move_box(self, box: Box, direction: str) -> bool:
        targets = box.targets(direction)
        target_contents: set[str | Box] = set(
            self.locations[target] for target in targets if target in self.locations)
        if WALL in target_contents:
            return False
        for target_box in target_contents:
            assert(isinstance(target_box, Box))
            if not self.can_move_box(target_box, direction):
                return False
        return True

    def move(self, direction: str):
        offset = DIRECTIONS[direction]
        target = self.current_pos.add(offset)
        
        target_contents = self.locations.get(target, None)
        if target_contents is None:
            self.current_pos = target
            return
        if target_contents == WALL:
            return
        assert(isinstance(target_contents, Box))

        if self.can_move_box(target_contents, direction):
            self.move_box(target_contents, direction)
            self.current_pos = target

    def sum_box_positions(self) -> int:
        boxes = set(contents for contents in self.locations.values() if isinstance(contents, Box))
        return sum(box.left.x + 100*box.left.y for box in boxes)
    
    def __str__(self) -> str:
        s = ''
        for y in range(self.height):
            for x in range(self.width):
                c = Coordinate(x,y)
                if c == self.current_pos:
                    s += '@'
                    continue
                contents = self.locations.get(c, None)
                if isinstance(contents, Box):
                    if contents.left == c:
                        s += '['
                    else:
                        s += ']'
                elif contents is None:
                    s += '.'
                else:
                    s += contents
            s += '\n'
        return s


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

    # print(map)

    for direction in move_input:
        map.move(direction)
        # print(map)

    # print(map)

    print('Sum of box GPS coordinates:', map.sum_box_positions())


if __name__ == '__main__':
    main()
