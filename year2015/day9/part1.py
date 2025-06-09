from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2015.day9.shared import SantaPlan


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        plan = SantaPlan(input)

        shortest_route = plan.shortest_path()

        log.log(log.RESULT, f'The shortest route is distance: {shortest_route}')
        return shortest_route


part = Part1()

part.add_result(605, r"""
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
""")

part.add_result(251)
