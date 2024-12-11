#!/usr/bin/python

import functools
from pathlib import Path

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'
TEST_INPUT = '125 17'


@functools.cache
def num_stones(value: int, blinks_remaining: int) -> int:
    if blinks_remaining == 0:
        return 1
    if value == 0:
        return num_stones(1, blinks_remaining - 1)
    s = str(value)
    if len(s) % 2 != 0:
        return num_stones(value * 2024, blinks_remaining - 1)
    n = len(s) // 2
    return num_stones(int(s[n:]), blinks_remaining - 1) + num_stones(int(s[:n]), blinks_remaining - 1)


def main():
    with INPUT_FILE.open() as ifp:
        input = list(map(int,
                # TEST_INPUT.split()
                ifp.readline().strip().split()
        ))

    total_stones = 0
    for value in input:
        total_stones += num_stones(value, 75)

    print('After 75 blinks the number of stones is:', total_stones)


if __name__ == '__main__':
    main()
