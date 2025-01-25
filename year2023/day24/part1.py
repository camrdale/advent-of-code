import itertools

import aoc.input
from aoc import log
import aoc.map
from aoc import runner

from year2023.day24 import shared


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()
        range_min: int
        range_max: int
        range_min, range_max = parser.get_additional_params()

        hailstones: list[shared.Hailstone] = []
        for line in input:
            hailstones.append(shared.Hailstone.from_text(line))
        
        intersections = 0
        for hail1, hail2 in itertools.combinations(hailstones, 2):
            if hail1.intersect(hail2, range_min, range_max):
                intersections += 1

        log.log(log.RESULT, f'Intersections withing the test area: {intersections}')
        return intersections


part = Part1()

part.add_result(2, r"""
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
""", 7, 27)

part.add_result(15593, None, 200000000000000, 400000000000000)
