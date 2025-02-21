from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2019 import intcode

PROGRAM = r"""NOT A T
OR T J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
"""


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))

        springdroid = intcode.SynchronousProgram('SPRINGDROID', intcode_input)

        log.log(log.DEBUG, f'SPRINGDROID initial output:')
        log.log(log.INFO, springdroid.get_latest_output_ascii())
        log.log(log.DEBUG, f'SPRINGDROID end of initial output')
        if springdroid.is_done():
            raise ValueError(f'SPRINGDROID exited early.')

        springdroid.write_ascii(PROGRAM)

        log.log(log.DEBUG, f'SPRINGDROID final output:')
        log.log(log.INFO, springdroid.get_latest_output_ascii())
        log.log(log.DEBUG, f'SPRINGDROID end of final output')

        hull_damage = springdroid.get_latest_output()[-1]
        log.log(log.RESULT, f'The amount of hull damage reported: {hull_damage}')
        return hull_damage


part = Part1()

part.add_result(19355391)
