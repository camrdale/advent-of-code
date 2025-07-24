from aoc.input import InputParser
from aoc.log import log, RESULT, DEBUG
from aoc.map import ParsedMap, Coordinate, Offset
from aoc.runner import Part

OBSTRUCTION = '#'

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

INCREMENTS = {
    UP: Offset(0, -1),
    RIGHT: Offset(1, 0),
    DOWN: Offset(0, 1),
    LEFT: Offset(-1, 0)}
STARTING_DIRECTIONS = {
    '^': UP, 
    '>': RIGHT, 
    'v': DOWN, 'V': DOWN, 
    '<': LEFT}


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        map = ParsedMap(input, OBSTRUCTION + ''.join(STARTING_DIRECTIONS.keys()))

        obstacles = map.features[OBSTRUCTION]

        starting_pos: Coordinate | None = None
        starting_direction = -1
        for direction in STARTING_DIRECTIONS.keys():
            if len(map.features[direction]) > 0:
                starting_pos = list(map.features[direction])[0]
                starting_direction = STARTING_DIRECTIONS[direction]

        if starting_pos is None:
            print('ERROR: malformed input')
            return -1
        log(DEBUG, map.min_x, map.min_y, map.max_x, map.max_y)

        direction = starting_direction
        current_pos = starting_pos
        visited_positions_direction: set[tuple[Coordinate, int]] = set([(starting_pos, starting_direction)])
        while True:
            next_pos = current_pos.add(INCREMENTS[direction])
            if not map.valid(next_pos):
                break
            if next_pos in obstacles:
                direction = (direction + 1) % 4
                continue
            current_pos = next_pos
            visited_positions_direction.add((current_pos, direction))

        num_visited = len(set(coordinate for coordinate, _ in visited_positions_direction))
        log(RESULT, 'Number of visited positions:', num_visited)
        return num_visited


part = Part1()

part.add_result(41, """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""")

part.add_result(4819)
