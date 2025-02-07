import itertools
import queue

import aoc.input
from aoc import log
from aoc import runner

from year2019 import intcode


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))

        max_thruster_signal = -1
        max_phase_sequence: tuple[int, ...] = ()
        for phase_sequence in itertools.permutations([0,1,2,3,4], 5):
            thruster_signal = 0
            for phase in phase_sequence:
                program = intcode.Program(f'Amp-{phase}', list(intcode_input))
                input_queue: queue.Queue[int] = queue.Queue()
                input_queue.put(phase)
                input_queue.put(thruster_signal)
                output_queue: queue.Queue[int] = queue.Queue()
                program.execute(input_queue, output_queue)
                program.join()
                thruster_signal = output_queue.get_nowait()
            if thruster_signal > max_thruster_signal:
                max_thruster_signal = thruster_signal
                max_phase_sequence = phase_sequence
                log.log(log.DEBUG, f'New max thruster signal {thruster_signal} for phase sequence: {",".join(map(str, phase_sequence))}')
        log.log(log.RESULT, f'Max thruster signal {max_thruster_signal} (from phase setting sequence {",".join(map(str, max_phase_sequence))})')
        return max_thruster_signal


part = Part1()

part.add_result(43210, r"""
3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
""")

part.add_result(54321, r"""
3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0
""")

part.add_result(65210, r"""
3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0
""")

part.add_result(51679)
