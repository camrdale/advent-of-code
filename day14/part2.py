#!/usr/bin/python

from pathlib import Path
import time

from shared import RobotMap

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'


def main():
    with INPUT_FILE.open() as ifp:
        robots = RobotMap(ifp.readlines(), 101, 103)

    found: list[tuple[tuple[int, int, int, int], int, str]] = []
    for elapsed in range(10000):
        robots.simulate(1)
        found.append((robots.line_lengths(), elapsed + 1, str(robots)))
    
    for line_lengths, elapsed, robots in sorted(found, reverse=True):
        print(f'Robots after {elapsed} seconds have longest line lengths {line_lengths}')
        print(robots)
        time.sleep(1)


if __name__ == '__main__':
    main()
