from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        sides = [list(map(int, line.split())) for line in input]

        possible = 0
        for group in range(0, len(input), 3):
            for column in range(3):
                triangle = [sides[row][column] for row in range(group, group+3)]
                longest = max(triangle)
                if sum(triangle) - longest > longest:
                    possible += 1

        log.log(log.RESULT, f'The number of possible triangles: {possible}')
        return possible


part = Part2()

part.add_result(6, """
101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603
""")

part.add_result(1849)
