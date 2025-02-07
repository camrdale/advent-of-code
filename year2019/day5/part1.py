import queue

import aoc.input
from aoc import log
from aoc import runner

from year2019 import intcode


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))

        program = intcode.Program('Diagnostic', list(intcode_input))
        input_queue: queue.Queue[int] = queue.Queue()
        input_queue.put(1)
        output_queue: queue.Queue[int] = queue.Queue()
        program.execute(input_queue, output_queue)
        program.join()

        output: list[int] = []
        while not output_queue.empty():
            output.append(output_queue.get_nowait())

        log.log(log.INFO, f'Input 1 outputs {output}')
        log.log(log.RESULT, f'Intcode program diagnostic code: {output[-1]}')
        return output[-1]


part = Part1()

part.add_result(16225258)
