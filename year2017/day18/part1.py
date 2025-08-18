import queue
import threading

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day18.shared import Computer, RcvOccurred


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        sounds: queue.SimpleQueue[int] = queue.SimpleQueue()
        duet = Computer(input, 0, sounds, sounds, threading.Event())

        try:
            duet.run()
        except RcvOccurred as e:
            log.log(log.RESULT, f'The first RCV value: {e.value}')
            return e.value
        
        raise ValueError(f'Failed to trigger a RCV')


part = Part1()

part.add_result(4, """
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
""")

part.add_result(3188)
