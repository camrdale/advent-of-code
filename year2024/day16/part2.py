from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from .shared import Coordinate, ReindeerMaze


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        estimated_iterations = parser.get_additional_params()[0]

        maze = ReindeerMaze(input)

        with log.ProgressBar(estimated_iterations=estimated_iterations, desc=f'day 16,2') as progress_bar:
            paths = maze.lowest_score_paths(progress_bar=progress_bar)

        if len(paths) == 0:
            print('ERROR failed to find path through the maze')
            exit(1)

        log.log(log.INFO, maze.print_paths(paths))
        log.log(log.INFO, 'Found', len(paths), 'lowest score paths with score:', paths[0].score)

        visited: set[Coordinate] = set()
        for path in paths:
            visited.update(path.previous)
        visited.add(maze.starting_pos)
        visited.add(maze.end_pos)

        log.log(log.RESULT, 'Tiles in all best paths:', len(visited))

        return len(visited)


part = Part2()

part.add_result(45, """
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

part.add_result(64, """
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

part.add_result(609, None, 362359)
