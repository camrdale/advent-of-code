from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day20.shared import Regex, FacilityMap


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()[0][1:-1]

        regex, _ = Regex.parse(input)
        assert input == repr(regex), f'"{input}" != "{repr(regex)}"'

        facility_map = FacilityMap(regex)
        log.log(log.INFO, facility_map.print_map)

        rooms = facility_map.rooms()

        num_doors = max(rooms.values())
        log.log(log.RESULT, f'The number of doors to get to furthest room: {num_doors}')
        return num_doors


part = Part1()

part.add_result(3, """
^WNE$
""")

part.add_result(10, """
^ENWWW(NEEE|SSE(EE|N))$
""")

part.add_result(18, """
^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$
""")

part.add_result(23, """
^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$
""")

part.add_result(31, """
^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$
""")

part.add_result(4214)
