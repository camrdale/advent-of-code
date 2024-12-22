from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part

from .shared import next_secret


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        sum_2000th = 0
        for line in input:
            secret = int(line)
            for _ in range(2000):
                secret = next_secret(secret)

            sum_2000th += secret

        log(RESULT, f'Sum of the 2000th secret numbers after: {sum_2000th}')
        return sum_2000th


part = Part1()

part.add_result(37327623, """
1
10
100
2024
""")

part.add_result(17005483322)
