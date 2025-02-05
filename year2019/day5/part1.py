import aoc.input
from aoc import log
from aoc import runner

from year2019 import intcode


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))

        program = intcode.Program(intcode_input)
        output = program.run([1])
        log.log(log.INFO, f'Input 1 outputs {output}')
        log.log(log.RESULT, f'Intcode program diagnostic code: {output[-1]}')
        return output[-1]


part = Part1()

part.add_result(16225258)
