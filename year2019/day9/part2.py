import queue

import aoc.input
from aoc import log
from aoc import runner

from year2019 import intcode


class Part2(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> list[int]:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))
        program_inputs: list[int] = parser.get_additional_params()[0]

        program = intcode.Program('BOOST', list(intcode_input))
        
        input_queue: queue.Queue[int] = queue.Queue()
        for program_input in program_inputs:
            input_queue.put(program_input)
        output_queue: queue.Queue[int] = queue.Queue()

        program.execute(input_queue, output_queue)
        program.join()

        output: list[int] = []
        while not output_queue.empty():
            output.append(output_queue.get_nowait())

        log.log(log.RESULT, f'Input {program_inputs} outputs {output}')
        return output


part = Part2()

part.add_result([66113], None, [2])
