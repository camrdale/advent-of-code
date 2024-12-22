import re

from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part

MUL_PATTERN = re.compile(r'mul\(([0-9]*),([0-9]*)\)')
DO_PATTERN = re.compile(r'do\(\)')
DONT_PATTERN = re.compile(r'don\'t\(\)')


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        raw_input = parser.get_input()
        input: list[str] = []
        for line in raw_input:
            for c in line:
                if c == 'm' or c == 'd':
                    input.append('')
                if len(input) == 0:
                    continue
                input[-1] += c

        enabled = True
        multiplications = 0
        for command in input:
            if DO_PATTERN.match(command) is not None:
                enabled = True
                continue
            if DONT_PATTERN.match(command) is not None:
                enabled = False
                continue
            if enabled:
                match = MUL_PATTERN.match(command)
                if match is not None:
                    (l, r) = match.group(1,2)
                    multiplications += int(l) * int(r)

        log(RESULT, 'Results of the enabled multiplications:', multiplications)
        return multiplications


part = Part2()

part.add_result(48, """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
""")

part.add_result(88811886)
