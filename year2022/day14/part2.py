from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day14.shared import CaveMap, Coordinate, ROCK


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        cave_map = CaveMap(input)
        floor = cave_map.max_y + 2
        for x in range(500 - floor - 2, 500 + floor + 3):
            cave_map.add_feature(ROCK, Coordinate(x, floor))
        log.log(log.DEBUG, cave_map.print_map())

        num_sand = 0
        while cave_map.add_sand():
            num_sand += 1
        log.log(log.DEBUG, cave_map.print_map())

        log.log(log.RESULT, f'The number of units of sand that come to rest: {num_sand}')
        return num_sand


part = Part2()

part.add_result(93, r"""
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""")

part.add_result(24377)
