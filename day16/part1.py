#!/usr/bin/python

from pathlib import Path

from shared import ReindeerMaze

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'
TEST_INPUT = """
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
"""


def main():
    with INPUT_FILE.open() as ifp:
        maze = ReindeerMaze(
                # TEST_INPUT.split('\n')
                ifp.readlines()
        )

    paths = maze.lowest_score_paths()

    if len(paths) == 0:
        print('ERROR failed to find path through the maze')
        exit(1)

    # print(maze.print_paths(paths[:1]))
    print('Found', len(paths), 'lowest score paths with score:', paths[0].score)


if __name__ == '__main__':
    main()
