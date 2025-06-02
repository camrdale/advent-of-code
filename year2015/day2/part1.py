import itertools

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        wrapping_paper = 0
        for line in input:
            dimensions = map(int, line.split('x'))
            smallest_side = 1000000000
            for dim1, dim2 in itertools.combinations(dimensions, 2):
                wrapping_paper += 2 * dim1 * dim2
                if dim1 * dim2 < smallest_side:
                    smallest_side = dim1 * dim2
            wrapping_paper += smallest_side

        log.log(log.RESULT, f'Total square feet of wrapping paper: {wrapping_paper}')
        return wrapping_paper


part = Part1()

part.add_result(58, """
2x3x4
""")

part.add_result(43, """
1x1x10
""")

part.add_result(1598415)
