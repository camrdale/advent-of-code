from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day17.shared import ClayMap, WATER


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        clay_map = ClayMap(parser.get_input())

        clay_map.flow()

        still_water = len(clay_map.features[WATER])
        log.log(log.RESULT, f'The number of tiles that water settles in: {still_water}')
        return still_water


part = Part2()

part.add_result(29, """
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
""")

part.add_result(24660)
