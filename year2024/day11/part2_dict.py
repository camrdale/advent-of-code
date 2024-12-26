#!/usr/bin/python

from collections import defaultdict
from pathlib import Path

import os, sys; sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from aoc.input import InputParser
from aoc.log import log, RESULT, INFO, DEBUG, set_log_level
from aoc.runner import Part


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


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = list(map(int, parser.get_input()[0].split()))

        stone_counts: dict[int, int] = defaultdict(int)
        for value in input:
            stone_counts[value] += 1
            
        log(DEBUG, stone_counts)

        for i in range(75):
            stone_counts = blink(stone_counts)
            log(INFO, 'After', i+1, 'blinks the number of stones is:', sum(stone_counts.values()))
            log(DEBUG, stone_counts)

        total_stones = sum(stone_counts.values())
        log(RESULT, 'After 75 blinks the number of stones is:', total_stones)
        return total_stones


part = Part2()

part.add_result(65601038650482, """
125 17
""")

part.add_result(221683913164898)


if __name__ == '__main__':
    set_log_level(RESULT)
    assert part.run_part(2024, 11, 2, subdirectory=Path(sys.argv[0]))
