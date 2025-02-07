import queue

import aoc.input
from aoc import log
from aoc import runner

from year2019 import intcode


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))

        replacements = parser.get_additional_params()
        for replacement in replacements:
            intcode_input[replacement[0]] = replacement[1]

        program = intcode.Program('GravityAssist', list(intcode_input))
        program.execute(queue.Queue(), queue.Queue())
        program.join()

        log.log(log.INFO, f'{input[0]} becomes {program.memory}')
        log.log(log.RESULT, f'Intcode program position 0: {program.memory[0]}')
        return program.memory[0]


part = Part1()

part.add_result(3500, r"""
1,9,10,3,2,3,11,0,99,30,40,50
""")

part.add_result(2, r"""
1,0,0,0,99
""")

part.add_result(2, r"""
2,3,0,3,99
""")

part.add_result(2, r"""
2,4,4,5,99,0
""")

part.add_result(30, r"""
1,1,1,4,99,5,6,0,99
""")

part.add_result(3562624, None, (1, 12), (2, 2))
