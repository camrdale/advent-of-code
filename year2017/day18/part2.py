import queue
import threading

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day18.shared import Computer


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        program0_input: queue.SimpleQueue[int] = queue.SimpleQueue()
        program1_input: queue.SimpleQueue[int] = queue.SimpleQueue()
        program0_blocked = threading.Event()
        program1_blocked = threading.Event()
        program0 = Computer(input, 0, program0_input, program1_input, program0_blocked, part1=False)
        program1 = Computer(input, 1, program1_input, program0_input, program1_blocked, part1=False)

        program0.start()
        program1.start()

        while True:
            program0_blocked.wait()
            program1_blocked.wait()
            if program0_blocked.is_set() and program1_blocked.is_set() and program0_input.qsize() == 0 and program1_input.qsize() == 0:
                log.log(log.RESULT, f'Deadlock, program 1 sent: {program1.state.num_sends}')
                return program1.state.num_sends


part = Part2()

part.add_result(3, """
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d
""")

part.add_result(7112)
