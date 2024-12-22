from pathlib import Path

from aoc.input import InputParser
from aoc.log import log, RESULT, DEBUG
from aoc.map import ParsedMap, Coordinate, Offset
from aoc.runner import Part

from .shared import Visualizer

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
    def __init__(self, visualize: bool = True):
        super().__init__()
        self.visualize = visualize

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
        visualizer: Visualizer | None = None
        if self.visualize:
            visualizer = Visualizer(map.width, map.height)

        direction = starting_direction
        current_pos = starting_pos
        visited_positions_direction: set[tuple[Coordinate, int]] = set([(starting_pos, starting_direction)])
        if visualizer is not None:
            visualizer.draw_board(obstacles, visited_positions_direction, current_pos, direction, 1)
        while True:
            next_pos = current_pos.add(INCREMENTS[direction])
            if not (0 <= next_pos[0] < map.width and 0 <= next_pos[1] < map.height):
                break
            if next_pos in obstacles:
                direction = (direction + 1) % 4
                continue
            if visualizer is not None:
                visualizer.animate_movement(obstacles, visited_positions_direction, current_pos, next_pos, direction, 1/60)
            current_pos = next_pos
            visited_positions_direction.add((current_pos, direction))

        if visualizer is not None:
            visualizer.animate_movement(obstacles, visited_positions_direction, current_pos, next_pos, direction, 1)

        num_visited = len(set(coordinate for coordinate, _ in visited_positions_direction))
        log(RESULT, 'Number of visited positions:', num_visited)

        if visualizer is not None:
            visualizer.finalize()
            visualizer.outputMovie(Path(__file__).parent.resolve() / 'part1.mp4')

        return num_visited


part = Part1(visualize=False)

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
