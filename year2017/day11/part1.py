from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate
from aoc.runner import Part

from year2017.day11.shared import HEX_NEIGHBORS, hex_distance


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()[0]

        hex_location = Coordinate(0, 0)
        for hex_neighbor in input.split(','):
            hex_location = hex_location.add(HEX_NEIGHBORS[hex_neighbor])

        steps = hex_distance(hex_location)
        log.log(log.RESULT, f'The child process is {steps} hexagonal steps away')
        return steps


part = Part1()

part.add_result(3, """
ne,ne,ne
""")

part.add_result(0, """
ne,ne,sw,sw
""")

part.add_result(2, """
ne,ne,s,s
""")

part.add_result(3, """
se,sw,se,sw,sw
""")

part.add_result(670)
