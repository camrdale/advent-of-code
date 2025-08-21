import numpy
import numpy.typing

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day21.shared import START, build_enhancements, enhance_matrix, to_string


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        num_iterations: int = parser.get_additional_params()[0]

        enhancements: dict[bytes, numpy.typing.NDArray[numpy.bool]] = build_enhancements(input)

        matrix = START
        for i in range(num_iterations):
            log.log(log.DEBUG, f'After {i} iterations')
            log.log(log.DEBUG, lambda: to_string(matrix))
            matrix = enhance_matrix(matrix, enhancements)

        log.log(log.INFO, f'Final matrix')
        log.log(log.INFO, lambda: to_string(matrix))

        pixels_on: int = matrix.sum()

        log.log(log.RESULT, f'The number of pixels on: {pixels_on}')
        return pixels_on


part = Part1()

part.add_result(12, """
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
##./#../... => #..#/..../..../#..#
""", 2)

part.add_result(208, None, 5)
