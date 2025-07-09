from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day9.shared import decompressed_length


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        length = decompressed_length(input[0])

        log.log(log.RESULT, f'The decompressed length of the file: {length}')
        return length


part = Part1()

part.add_result(6, """
ADVENT
""")

part.add_result(7, """
A(1x5)BC
""")

part.add_result(9, """
(3x3)XYZ
""")

part.add_result(11, """
A(2x2)BCD(2x2)EFG
""")

part.add_result(6, """
(6x1)(1x3)A
""")

part.add_result(18, """
X(8x2)(3x3)ABCY
""")

part.add_result(99145)
