import numpy
import numpy.typing

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day21.shared import START, build_enhancements, enhance_matrix


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        num_iterations: int = parser.get_additional_params()[0]

        enhancements: dict[bytes, numpy.typing.NDArray[numpy.bool]] = build_enhancements(input)

        matrix = START
        for i in range(num_iterations):
            log.log(log.INFO, f'After {i} iterations, matrix has size: {matrix.shape[0]}')
            matrix = enhance_matrix(matrix, enhancements)

        log.log(log.INFO, f'Final matrix has size: {matrix.shape[0]}')

        pixels_on: int = matrix.sum()

        log.log(log.RESULT, f'The number of pixels on: {pixels_on}')
        return pixels_on


part = Part2()

part.add_result(2480380, None, 18)
