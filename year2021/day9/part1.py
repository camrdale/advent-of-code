import numpy

from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        inputarray = [list(map(int, line)) for line in input]
        width = len(inputarray[0])
        height = len(inputarray)

        matrix = numpy.array(inputarray).reshape(height, width)

        # Matrices shifted by one in all four directions, filled with 10s.
        down = numpy.insert(numpy.delete(matrix, 0, axis=0), height-1, 10, axis=0)
        up = numpy.vstack([numpy.tile(10, [1, width]), matrix[:-1, :]])
        left = numpy.tile(10, [height, width])
        left[:, :-1] = matrix[:, 1:]
        right = numpy.tile(10, [height, width])
        right[:, 1:] = matrix[:, :-1]

        # Create a vectorized function that will look at the four neighbors of a location.
        def risklevel(i: int, downi: int, upi: int, lefti: int, righti: int):
            if i < min(downi, upi, lefti, righti):
                return i + 1
            return 0

        vfunc_risklevel = numpy.vectorize(risklevel)
        output = vfunc_risklevel(matrix, down, up, left, right)

        sum_of_risk_levels = numpy.sum(output)
        log(RESULT, "sum of risk levels:", sum_of_risk_levels)
        return sum_of_risk_levels


part = Part1()

part.add_result(15, """
2199943210
3987894921
9856789892
8767896789
9899965678
""")

part.add_result(564)
