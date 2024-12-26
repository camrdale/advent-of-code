from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part

from .shared import Coordinate, ReindeerMaze


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        maze = ReindeerMaze(input)

        paths = maze.lowest_score_paths()

        if len(paths) == 0:
            print('ERROR failed to find path through the maze')
            exit(1)

        log(INFO, maze.print_paths(paths))
        log(INFO, 'Found', len(paths), 'lowest score paths with score:', paths[0].score)

        visited: set[Coordinate] = set()
        for path in paths:
            visited.update(path.previous)
        visited.add(maze.starting_pos)
        visited.add(maze.end_pos)

        log(RESULT, 'Tiles in all best paths:', len(visited))

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
""")

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
""")

part.add_result(609)
