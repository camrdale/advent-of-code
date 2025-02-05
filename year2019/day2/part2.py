import aoc.input
from aoc import log
from aoc import runner

from year2019 import intcode


class Part2(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))

        for noun in range(100):
            for verb in range(100):
                intcode_input[1] = noun
                intcode_input[2] = verb

                program = intcode.Program(list(intcode_input))
                program.run([])
                if program.memory[0] == 19690720:
                    log.log(log.RESULT, f'Noun {noun} and verb {verb} results in output {program.memory[0]}: {100 * noun + verb}')
                    return 100 * noun + verb
                log.log(log.INFO, f'Noun {noun} and verb {verb} results in output {program.memory[0]}')

        raise ValueError(f'Failed to find noun and verb that produces 19690720')


part = Part2()

part.add_result(8298)
