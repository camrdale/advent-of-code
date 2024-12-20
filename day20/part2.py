#!/usr/bin/python

from pathlib import Path

from shared import Racetrack

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'
TEST_INPUT = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""


def main():
    with INPUT_FILE.open() as ifp:
        racetrack = Racetrack(
                # TEST_INPUT.split('\n')
                ifp.readlines()
        )

    all_cheats = racetrack.all_cheats(20)

    for saved_time, cheats in sorted(all_cheats.items()):
        if saved_time >= 100:
            break
        print(f'There are {len(cheats)} cheats that save {saved_time} picoseconds.')

    print('Number of cheats that save at least 100ps:',
          sum(len(cheats) for saved_time, cheats in all_cheats.items() if saved_time >= 100))


if __name__ == '__main__':
    main()
