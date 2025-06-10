from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2015.day10.shared import conway_look_and_say


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        result = conway_look_and_say(input[0], 50)

        log.log(log.RESULT, f'The length of the result: {result}')
        return result


part = Part2()

part.add_result(6989950, '1321131112')
