from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day24.shared import AirDuctMap


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        air_ducts = AirDuctMap(input)

        result = air_ducts.all_locations_route()

        log.log(log.RESULT, f'The fewest number of steps to visit all locations: {result}')
        return result


part = Part1()

part.add_result(14, """
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
""")

part.add_result(464)
