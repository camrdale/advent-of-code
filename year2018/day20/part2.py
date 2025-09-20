from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day20.shared import Regex, FacilityMap


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()[0][1:-1]

        regex, _ = Regex.parse(input)
        assert input == repr(regex), f'"{input}" != "{repr(regex)}"'

        facility_map = FacilityMap(regex)
        log.log(log.INFO, facility_map.print_map)

        rooms = facility_map.rooms()

        num_1000_doors = len([doors for doors in rooms.values() if doors >= 1000])
        log.log(log.RESULT, f'The number of rooms at least 1000 doors away: {num_1000_doors}')
        return num_1000_doors


part = Part2()

part.add_result(8492)
