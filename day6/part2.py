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


def contains_loop(obstacles: set[Coordinate], pos: Coordinate, direction: int, width: int, height: int) -> bool:
    visited_positions_direction: set[tuple[Coordinate, int]] = set([(pos, direction)])
    while True:
        next_pos = pos.add(INCREMENTS[direction])
        if not next_pos.valid(width, height):
            return False
        if next_pos in obstacles:
            direction = (direction + 1) % 4
            continue
        if (next_pos, direction) in visited_positions_direction:
            return True

        pos = next_pos
        visited_positions_direction.add((pos, direction))


class Part2(Part):
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
        log(DEBUG, map.width, map.height)

        direction = starting_direction
        current_pos = starting_pos
        visited_positions = set([starting_pos])
        looping_obstacles: set[tuple[int, int]] = set()
        while True:
            next_pos = current_pos.add(INCREMENTS[direction])
            if not map.valid(next_pos):
                break
            if next_pos in obstacles:
                direction = (direction + 1) % 4
                continue

            if next_pos not in visited_positions and contains_loop(obstacles | set([next_pos]), current_pos, direction, map.width, map.height):
                looping_obstacles.add(next_pos)

            current_pos = next_pos
            visited_positions.add(current_pos)

        log(RESULT, 'Number of candidate positions to create a loop:', len(looping_obstacles))
        return len(looping_obstacles)


part = Part2()

part.add_result(6, """
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

part.add_result(1796)
