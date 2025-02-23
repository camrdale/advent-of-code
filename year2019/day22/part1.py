import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

CUT = re.compile(r'cut ([0-9-]*)')
DEAL_NEW_STACK = re.compile(r'deal into new stack')
DEAL_WITH_INCREMENT = re.compile(r'deal with increment ([0-9]*)')

N = 10007


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        # y = m*x + b  (x = starting position, y = ending position)
        m = 1
        b = 0
        for line in input:
            if match := DEAL_NEW_STACK.match(line):
                m = (-m) % N
                b = (-b - 1) % N
            elif match := CUT.match(line):
                cut = int(match.group(1))
                b = (b - cut) % N
            elif match := DEAL_WITH_INCREMENT.match(line):
                increment = int(match.group(1))
                m = (m * increment) % N
                b = (b * increment) % N
            else:
                raise ValueError(f'Unparseable line: {line}')

        final_position = (m * 2019 + b) % N
        log.log(log.INFO, f'{final_position} = ({m}*2019 + {b}) % {N} = {m * 2019 + b} % {N}')
        log.log(log.RESULT, f'Final position of card 2019: {final_position}')

        return final_position


part = Part1()

part.add_result(4775)
