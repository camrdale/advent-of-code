import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


TARGET = re.compile(r'target area: x=([0-9-]*)..([0-9-]*), y=([0-9-]*)..([0-9-]*)')


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        match = TARGET.match(input[0])
        assert match is not None

        y_min = int(match.group(3))

        max_y_velocity = abs(y_min) - 1
        max_height = max_y_velocity * (max_y_velocity + 1) // 2

        log.log(log.RESULT, 'The highest achievable y position reached:', max_height)
        return max_height


part = Part1()

part.add_result(45, """
target area: x=20..30, y=-10..-5
""")

part.add_result(5050)
