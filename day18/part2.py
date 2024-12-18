#!/usr/bin/python

from pathlib import Path

from shared import ReindeerMaze, Coordinate

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'
TEST_INPUT = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""


def main():
    with INPUT_FILE.open() as ifp:
        maze, num_fall, input = ReindeerMaze(
                # 7, 7), 12, TEST_INPUT.split('\n')
                71, 71), 1024, ifp.readlines()

    bytes = [
        Coordinate(*map(int, line.strip().split(',')))
        for line in input
        if len(line.strip()) > 0]

    maze.add_walls(bytes[:num_fall])

    path = maze.lowest_score_path()

    if path is None:
        print('ERROR failed to find initial path through the maze')
        exit(1)

    next_to_fall = num_fall
    while next_to_fall < len(bytes):
        next_byte = bytes[next_to_fall]
        maze.add_walls((next_byte,))
        if next_byte in path.previous:
            path = maze.lowest_score_path()
            if path is None:
                print(f'Path is not possible after {next_to_fall} byte: {next_byte}')
                break
        next_to_fall += 1


if __name__ == '__main__':
    main()
