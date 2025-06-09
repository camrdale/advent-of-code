from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2015.day9.shared import SantaPlan


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        plan = SantaPlan(input)

        shortest_route = plan.longest_path()

        log.log(log.RESULT, f'The longest route is distance: {shortest_route}')
        return shortest_route


part = Part2()

part.add_result(982, r"""
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
""")

part.add_result(898)
