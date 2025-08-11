from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate
from aoc.runner import Part

from year2017.day11.shared import HEX_NEIGHBORS, hex_distance


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()[0]

        max_distance = 0
        hex_location = Coordinate(0, 0)
        for hex_neighbor in input.split(','):
            hex_location = hex_location.add(HEX_NEIGHBORS[hex_neighbor])
            distance = hex_distance(hex_location)
            if distance > max_distance:
                max_distance = distance

        log.log(log.RESULT, f'The furthest away the child process got is {max_distance} hexagonal steps away')
        return max_distance


part = Part2()

part.add_result(1426)
