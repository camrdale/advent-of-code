from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.knot_hash import knot_hash


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()[0]

        used_squares = 0
        for row in range(128):
            l = knot_hash(f'{input}-{row}')
            for i in l:
                used_squares += i.bit_count()

        log.log(log.RESULT, f'The number of used squares: {used_squares}')
        return used_squares


part = Part1()

part.add_result(8108, """
flqrgnkx
""")

part.add_result(8216, """
nbysizxe
""")
