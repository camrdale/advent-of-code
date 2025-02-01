import aoc.input
from aoc import log
from aoc import runner


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()

        total_fuel = 0
        for line in input:
            mass = int(line)
            fuel = mass // 3 - 2
            total_fuel += fuel

        log.log(log.RESULT, f'Total fuel needed: {total_fuel}')
        return total_fuel


part = Part1()

part.add_result(2, r"""
12
""")

part.add_result(2, r"""
14
""")

part.add_result(654, r"""
1969
""")

part.add_result(33583, r"""
100756
""")

part.add_result(3325342)
