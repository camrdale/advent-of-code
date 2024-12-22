from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
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


class WarehouseMap(ParsedMap):
    def __init__(self, lines: list[str]):
        super().__init__(lines, WALL + BOX + ROBOT)
        self.current_pos: Coordinate
        (self.current_pos,) = self.features[ROBOT]
        self.locations: dict[Coordinate, str] = dict.fromkeys(self.features[WALL], WALL)
        self.locations.update(dict.fromkeys(self.features[BOX], BOX))

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
    
    def print_updated_map(self) -> str:
        self.features[WALL] = set(coord for coord, contents in self.locations.items() if contents == WALL)
        self.features[BOX] = set(coord for coord, contents in self.locations.items() if contents == BOX)
        self.features[ROBOT] = set([self.current_pos])
        return super().print_map()


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        map_input: list[str] = []
        move_input = ''
        map_time = True
        for line in input:
            if map_time:
                if line == '':
                    map_time = False
                else:
                    map_input.append(line)
            else:
                move_input += line

        map = WarehouseMap(map_input)

        for direction in move_input:
            map.move(direction)

        log(INFO, map.print_updated_map())

        box_positions = map.sum_box_positions()
        log(RESULT, 'Sum of box GPS coordinates:', box_positions)

        return box_positions


part = Part1()

part.add_result(2028, """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
""")

part.add_result(10092, """
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

part.add_result(1451928)
