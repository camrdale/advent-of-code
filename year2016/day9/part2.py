from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day9.shared import decompressed_length


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        length = decompressed_length(input[0], recursive=True)

        log.log(log.RESULT, f'The decompressed length of the file: {length}')
        return length


part = Part2()

part.add_result(9, """
(3x3)XYZ
""")

part.add_result(20, """
X(8x2)(3x3)ABCY
""")

part.add_result(241920, """
(27x12)(20x12)(13x14)(7x10)(1x12)A
""")

part.add_result(445, """
(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN
""")

part.add_result(10943094568)
