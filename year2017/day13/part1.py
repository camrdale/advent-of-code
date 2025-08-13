from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        severity = 0
        for line in input:
            depth, range = map(int, line.split(': '))
            if depth % ((range - 1) * 2) == 0:
                severity += depth * range

        log.log(log.RESULT, f'The total severity of the trip: {severity}')
        return severity


part = Part1()

part.add_result(24, """
0: 3
1: 2
4: 4
6: 4
""")

part.add_result(1528)
