from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day11.shared import ContainmentArea


EXTRA_PARTS = r"""
An elerium generator.
An elerium-compatible microchip.
A dilithium generator.
A dilithium-compatible microchip.
"""


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        containment_area = ContainmentArea(input)
        for extra_part in EXTRA_PARTS.split('\n'):
            if extra_part:
                containment_area.add_item(0, extra_part)

        result = containment_area.shortest_path()

        log.log(log.RESULT, f'The minimum number of steps to bring all objects to the top floor: {result}')
        return result


part = Part2()

part.add_result(61)
