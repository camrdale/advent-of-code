from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day23.shared import Computer


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        coprocessor = Computer(input)

        coprocessor.run()

        log.log(log.RESULT, f'The number of mul instructions invoked: {coprocessor.state.num_mul}')
        return coprocessor.state.num_mul


part = Part1()

part.add_result(6724)
