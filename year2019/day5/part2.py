import queue

import aoc.input
from aoc import log
from aoc import runner

from year2019 import intcode


class Part2(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))
        program_input: int = parser.get_additional_params()[0]

        program = intcode.Program('Diagnostic', list(intcode_input))
        input_queue: queue.Queue[int] = queue.Queue()
        input_queue.put(program_input)
        output_queue: queue.Queue[int] = queue.Queue()
        program.execute(input_queue, output_queue)
        program.join()

        output: list[int] = []
        while not output_queue.empty():
            output.append(output_queue.get_nowait())

        log.log(log.INFO, f'Input {program_input} outputs {output}')
        log.log(log.RESULT, f'Intcode program diagnostic code: {output[-1]}')
        return output[-1]


part = Part2()

part.add_result(1, r"""
3,9,8,9,10,9,4,9,99,-1,8
""", 8)

part.add_result(0, r"""
3,9,8,9,10,9,4,9,99,-1,8
""", 7)

part.add_result(1, r"""
3,9,7,9,10,9,4,9,99,-1,8
""", 7)

part.add_result(0, r"""
3,9,7,9,10,9,4,9,99,-1,8
""", 8)

part.add_result(1, r"""
3,3,1108,-1,8,3,4,3,99
""", 8)

part.add_result(0, r"""
3,3,1108,-1,8,3,4,3,99
""", 7)

part.add_result(1, r"""
3,3,1107,-1,8,3,4,3,99
""", 7)

part.add_result(0, r"""
3,3,1107,-1,8,3,4,3,99
""", 8)

part.add_result(0, r"""
3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9
""", 0)

part.add_result(1, r"""
3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9
""", -1)

part.add_result(0, r"""
3,3,1105,-1,9,1101,0,0,12,4,12,99,1
""", 0)

part.add_result(1, r"""
3,3,1105,-1,9,1101,0,0,12,4,12,99,1
""", 1)

part.add_result(2808771, None, 5)
