from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate
from aoc.runner import Part

from year2018.day17.shared import ClayMap, WATER, FLOW


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        clay_map = ClayMap(parser.get_input())

        log.log(log.DEBUG, lambda: clay_map.print_map(additional_features={
            '+': {Coordinate(500, clay_map.min_y)}}))
        
        clay_map.flow()

        total_water = len(clay_map.features[WATER] | clay_map.features[FLOW])
        log.log(log.RESULT, f'The number of tiles that water can reach: {total_water}')
        return total_water


part = Part1()

part.add_result(57, """
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
""")

part.add_result(29802)
