from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part

from .shared import ReindeerMaze


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        maze = ReindeerMaze(input)

        paths = maze.lowest_score_paths()

        if len(paths) == 0:
            print('ERROR failed to find path through the maze')
            exit(1)

        log(INFO, maze.print_paths(paths[:1]))
        log(RESULT, 'Found', len(paths), 'lowest score paths with score:', paths[0].score)

        return paths[0].score


part = Part1()

part.add_result(7036, """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
""")

part.add_result(11048, """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
""")

part.add_result(98520)
