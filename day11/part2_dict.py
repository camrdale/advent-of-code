#!/usr/bin/python

from collections import defaultdict
from pathlib import Path

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'
TEST_INPUT = '125 17'


def blink(stone_counts: dict[int, int]) -> dict[int, int]:
    new_counts: dict[int, int] = defaultdict(int)
    for value, count in stone_counts.items():
        if value == 0:
            new_counts[1] += count
            continue
        s = str(value)
        if len(s) % 2 != 0:
            new_counts[value * 2024] += count
            continue
        n = len(s) // 2
        new_counts[int(s[n:])] += count
        new_counts[int(s[:n])] += count
    return new_counts


def main():
    with INPUT_FILE.open() as ifp:
        input = list(map(int,
                # TEST_INPUT.split()
                ifp.readline().strip().split()
        ))

    stone_counts: dict[int, int] = defaultdict(int)
    for value in input:
        stone_counts[value] += 1
        
    # print(stone_counts)

    for i in range(75):
        stone_counts = blink(stone_counts)
        print('After', i+1, 'blinks the number of stones is:', sum(stone_counts.values()))
        # print(stone_counts)


if __name__ == '__main__':
    main()
