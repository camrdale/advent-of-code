import math

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        ribbon = 0
        for line in input:
            dimensions = sorted(list(map(int, line.split('x'))))
            ribbon += 2 * dimensions[0] + 2 * dimensions[1]
            ribbon += math.prod(dimensions)

        log.log(log.RESULT, f'Total feet of ribbon: {ribbon}')
        return ribbon


part = Part2()

part.add_result(34, """
2x3x4
""")

part.add_result(14, """
1x1x10
""")

part.add_result(3812909)
