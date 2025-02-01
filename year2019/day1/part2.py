import aoc.input
from aoc import log
from aoc import runner


def fuel(mass: int) -> int:
    initial_fuel = mass // 3 - 2
    if initial_fuel <= 0:
        return 0
    return initial_fuel + fuel(initial_fuel)


class Part2(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()

        total_fuel = 0
        for line in input:
            mass = int(line)
            mass_fuel = fuel(mass)
            total_fuel += mass_fuel

        log.log(log.RESULT, f'Total fuel needed: {total_fuel}')
        return total_fuel


part = Part2()

part.add_result(2, r"""
12
""")

part.add_result(2, r"""
14
""")

part.add_result(966, r"""
1969
""")

part.add_result(50346, r"""
100756
""")

part.add_result(4985158)
