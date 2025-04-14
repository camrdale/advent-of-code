from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from .shared import ReindeerMaze


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        estimated_iterations = parser.get_additional_params()[0]

        maze = ReindeerMaze(input)

        with log.ProgressBar(estimated_iterations=estimated_iterations, desc=f'day 16,1') as progress_bar:
            paths = maze.lowest_score_paths(progress_bar=progress_bar)

        if len(paths) == 0:
            print('ERROR failed to find path through the maze')
            exit(1)

        log.log(log.INFO, maze.print_paths(paths[:1]))
        log.log(log.RESULT, 'Found', len(paths), 'lowest score paths with score:', paths[0].score)

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
""", 289)

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
""", 181)

part.add_result(98520, None, 362359)
