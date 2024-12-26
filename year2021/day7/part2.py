import sys

from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        positions = [int(i) for i in input[0].split(',')]

        min_sum = sys.maxsize
        min_position = 0

        for current_position in range(min(positions), max(positions) + 1):
            cheat = sum(
                abs(current_position - pos)*(abs(current_position - pos) + 1)//2
                for pos in positions)
            if cheat <= min_sum:
                min_sum = cheat
                min_position = current_position
            else:
                break

        log(RESULT, 'Min cost of', min_sum, 'found at position', min_position)
        return min_sum


part = Part2()

part.add_result(168, """
16,1,2,0,4,2,7,1,2,14
""")

part.add_result(93699985)
