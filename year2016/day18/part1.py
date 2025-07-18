from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day18.shared import count_safe_tiles


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()[0]
        num_rows = parser.get_additional_params()[0]

        num_safe = count_safe_tiles(input, num_rows)

        log.log(log.RESULT, f'The number of safe tiles: {num_safe}')
        return num_safe


part = Part1()

part.add_result(6, """
..^^.
""", 3)

part.add_result(38, """
.^^.^.^^^^
""", 10)

part.add_result(1961, None, 40)
