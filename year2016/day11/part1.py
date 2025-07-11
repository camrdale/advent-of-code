from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day11.shared import ContainmentArea


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        containment_area = ContainmentArea(input)

        result = containment_area.shortest_path()

        log.log(log.RESULT, f'The minimum number of steps to bring all objects to the top floor: {result}')
        return result


part = Part1()

part.add_result(11, """
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.
""")

part.add_result(37)
