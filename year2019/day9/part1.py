import queue

import aoc.input
from aoc import log
from aoc import runner

from year2019 import intcode


class Part1(runner.Part):
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


part = Part1()

part.add_result([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], r"""
109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99
""", [])

part.add_result([1219070632396864], r"""
1102,34915192,34915192,7,4,7,99,0
""", [])

part.add_result([1125899906842624], r"""
104,1125899906842624,99
""", [])

part.add_result([2941952859], None, [1])
