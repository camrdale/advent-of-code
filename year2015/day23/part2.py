from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2015.day23.shared import Computer


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        computer = Computer(input)

        registers = computer.run(a=1)

        log.log(log.RESULT, f'Registers contain: {registers}')
        return registers['b']


part = Part2()

part.add_result(231)
