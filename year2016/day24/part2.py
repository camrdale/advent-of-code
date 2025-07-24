from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day24.shared import AirDuctMap


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        air_ducts = AirDuctMap(input)

        result = air_ducts.all_locations_and_back_route()

        log.log(log.RESULT, f'The fewest number of steps to visit all locations and return to the start: {result}')
        return result


part = Part2()

part.add_result(20, """
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
""")

part.add_result(652)
