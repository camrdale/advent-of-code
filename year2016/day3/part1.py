from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        possible = 0
        for line in input:
            sides = list(map(int, line.split()))
            longest = max(sides)
            if sum(sides) - longest > longest:
                possible += 1

        log.log(log.RESULT, f'The number of possible triangles: {possible}')
        return possible


part = Part1()

part.add_result(1, """
5 10 25
10 10 12
""")

part.add_result(993)
