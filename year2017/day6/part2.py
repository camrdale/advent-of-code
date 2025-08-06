from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day6.shared import redistribute_until_loop


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        blocks = list(map(int, input[0].split()))

        start_cycle, total_cycles = redistribute_until_loop(blocks)

        log.log(log.RESULT, f'Loop detected from cycles {start_cycle} to {total_cycles} of length: {total_cycles - start_cycle}')
        return total_cycles - start_cycle


part = Part2()

part.add_result(4, """
0  2  7  0
""")

part.add_result(2392)
