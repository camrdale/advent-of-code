from aoc.input import InputParser
from aoc.runner import Part

from .shared import lanternfish


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        starting_fish = [int(i) for i in input[0].split(',')]

        return lanternfish(starting_fish, 256)


part = Part2()

part.add_result(26984457539, """
3,4,3,1,2
""")

part.add_result(1708791884591)
