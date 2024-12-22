import re

from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part

MUL_PATTERN = re.compile(r'mul\(([0-9]*),([0-9]*)\)')


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        raw_input = parser.get_input()

        input: list[str] = []
        for line in raw_input:
            for c in line:
                if c == 'm':
                    input.append('')
                if len(input) == 0:
                    continue
                input[-1] += c

        multiplications = 0
        for mul in input:
            match = MUL_PATTERN.match(mul)
            if match is None:
                continue
            (l, r) = match.group(1,2)
            multiplications += int(l) * int(r)

        log(RESULT, 'Results of the multiplications:', multiplications)
        return multiplications
    

part = Part1()

part.add_result(161, """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
""")

part.add_result(166357705)
