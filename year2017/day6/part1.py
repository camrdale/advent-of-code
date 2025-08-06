from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day6.shared import redistribute_until_loop


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        blocks = list(map(int, input[0].split()))

        _, total_cycles = redistribute_until_loop(blocks)

        log.log(log.RESULT, f'Loop detected after {total_cycles} redistribution cycles: {blocks}')
        return total_cycles


part = Part1()

part.add_result(5, """
0  2  7  0
""")

part.add_result(6681)
