from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2019 import intcode

PROGRAM = r"""OR I J
OR F J
AND E J
OR H J
OR A T
AND B T
AND C T
NOT T T
AND T J
AND D J
RUN
"""


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))

        springdroid = intcode.SynchronousProgram('SPRINGDROID', intcode_input)

        log.log(log.DEBUG, f'SPRINGDROID initial output:')
        log.log(log.INFO, springdroid.get_latest_output_ascii())
        log.log(log.DEBUG, f'SPRINGDROID end of initial output')
        if springdroid.is_done():
            raise ValueError(f'SPRINGDROID exited early.')

        log.log(log.INFO, PROGRAM)
        springdroid.write_ascii(PROGRAM)

        log.log(log.DEBUG, f'SPRINGDROID final output:')
        log.log(log.INFO, springdroid.get_latest_output_ascii())
        log.log(log.DEBUG, f'SPRINGDROID end of final output')

        hull_damage = springdroid.get_latest_output()[-1]
        log.log(log.RESULT, f'The amount of hull damage reported: {hull_damage}')
        return hull_damage


part = Part2()

part.add_result(1143770635)
