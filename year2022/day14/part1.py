from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day14.shared import CaveMap


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        cave_map = CaveMap(input)
        log.log(log.DEBUG, cave_map.print_map())

        num_sand = 0
        while cave_map.add_sand():
            num_sand += 1
        log.log(log.DEBUG, cave_map.print_map())

        log.log(log.RESULT, f'The number of units of sand that come to rest: {num_sand}')
        return num_sand


part = Part1()

part.add_result(24, r"""
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""")

part.add_result(578)
