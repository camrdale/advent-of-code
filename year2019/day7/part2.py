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
        for phase_sequence in itertools.permutations([5,6,7,8,9], 5):
            programs: list[intcode.Program] = []
            queues: list[queue.Queue[int]] = [queue.Queue() for _ in range(len(phase_sequence))]

            for i, phase in enumerate(phase_sequence):
                program = intcode.Program(f'Amp-{i+1}', list(intcode_input))
                input_queue = queues[i]
                output_queue = queues[(i+1) % len(phase_sequence)]
                input_queue.put(phase)
                program.execute(input_queue, output_queue)
                programs.append(program)

            queues[0].put(0)
            for program in programs:
                program.join()
            thruster_signal = queues[0].get_nowait()

            if thruster_signal > max_thruster_signal:
                max_thruster_signal = thruster_signal
                max_phase_sequence = phase_sequence
                log.log(log.DEBUG, f'New max thruster signal {thruster_signal} for phase sequence: {",".join(map(str, phase_sequence))}')
        log.log(log.RESULT, f'Max thruster signal {max_thruster_signal} (from phase setting sequence {",".join(map(str, max_phase_sequence))})')
        return max_thruster_signal


part = Part1()

part.add_result(139629729, r"""
3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
""")

part.add_result(18216, r"""
3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
""")

part.add_result(19539216)
