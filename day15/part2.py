from typing import NamedTuple

from aoc.input import InputParser
from aoc.log import log, RESULT, INFO, DEBUG
from aoc.map import ParsedMap, Coordinate, Offset
from aoc.runner import Part

WALL = '#'
BOX = 'O'
ROBOT = '@'

UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'


DIRECTIONS = {
    UP: Offset(0, -1),
    RIGHT: Offset(1, 0),
    DOWN: Offset(0, 1),
    LEFT: Offset(-1, 0)}


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


class WarehouseMap(ParsedMap):
    def __init__(self, lines: list[str]):
        super().__init__(lines, WALL + BOX + ROBOT)
        self.current_pos: Coordinate
        (self.current_pos,) = self.features[ROBOT]
        self.current_pos = self.current_pos._replace(x=self.current_pos.x*2)
        self.locations: dict[Coordinate, str | Box] = {}

        self.width *= 2

        for coord in self.features[WALL]:
            self.locations[coord._replace(x=2*coord.x)] = WALL
            self.locations[coord._replace(x=2*coord.x + 1)] = WALL
        for coord in self.features[BOX]:
            box = Box(coord._replace(x=2*coord.x))
            for location in box.occupies():
                self.locations[location] = box

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
    
    def print_updated_map(self) -> str:
        self.features[WALL] = set(coord for coord, contents in self.locations.items() if contents == WALL)
        self.features[BOX] = set()
        self.features[ROBOT] = set([self.current_pos])
        additional_features: dict[str, set[Coordinate]] = {'[': set(), ']': set()}
        for location, contents in self.locations.items():
            if isinstance(contents, Box):
                if contents.left == location:
                    additional_features['['].add(location)
                else:
                    additional_features[']'].add(location)
        return super().print_map(additional_features)


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        map_input, move_input = parser.get_two_part_input()
        move_input = ''.join(move_input)

        map = WarehouseMap(map_input)

        log(DEBUG, map.print_updated_map())

        for direction in move_input:
            map.move(direction)
            log(DEBUG, map.print_updated_map())

        log(INFO, map.print_updated_map())

        box_positions = map.sum_box_positions()
        log(RESULT, 'Sum of box GPS coordinates:', box_positions)

        return box_positions


part = Part2()

part.add_result(618, """
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
""")

part.add_result(9021, """
##########
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
""")

part.add_result(1462788)
