import re

import numpy

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


INSTRUCTION = re.compile(r'(turn on|toggle|turn off) ([0-9]*),([0-9]*) through ([0-9]*),([0-9]*)')


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        lights = numpy.zeros((1000, 1000), dtype=numpy.int8)
        for line in input:
            instruction = INSTRUCTION.match(line)
            if instruction is None:
                raise ValueError(f'Failed to parse: {line}')

            x1, y1, x2, y2 = map(int, instruction.groups()[1:])
            assert x2 >= x1
            assert y2 >= y1
            
            delta = 0
            match instruction.group(1):
                case 'turn on':
                    delta = 1
                case 'turn off':
                    delta = -1
                case 'toggle':
                    delta = 2
                case _:
                    raise ValueError(f'Unexpected instruction "{instruction.group(1)}": {line}')

            new_lights = numpy.zeros((1000, 1000), dtype=numpy.int8)
            new_lights[x1:x2+1, y1:y2+1] = delta

            lights = numpy.clip(lights + new_lights, 0, None)

        total_brightness = lights.sum()
        log.log(log.RESULT, f'The total brightness of all lights: {total_brightness}')
        return total_brightness


part = Part1()

part.add_result(1000000, """
turn on 0,0 through 999,999
""")

part.add_result(2000, """
toggle 0,0 through 999,0
""")

part.add_result(0, """
turn off 499,499 through 500,500
""")

part.add_result(1000000 + 2000 - 4, """
turn on 0,0 through 999,999
toggle 0,0 through 999,0
turn off 499,499 through 500,500
""")

part.add_result(17836115)
