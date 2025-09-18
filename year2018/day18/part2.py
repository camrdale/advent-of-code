from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day18.shared import WoodedArea


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        area = WoodedArea(input)
        log.log(log.INFO, area.print)

        area.iterate(1_000_000_000)

        log.log(log.INFO, area.print)

        resource_value = area.resource_value()
        log.log(log.RESULT, f'The resource value after 1 billion minutes: {resource_value}')
        return resource_value


part = Part2()

part.add_result(210796)
