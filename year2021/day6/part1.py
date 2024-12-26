from aoc.input import InputParser
from aoc.runner import Part

from .shared import lanternfish


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        starting_fish = [int(i) for i in input[0].split(',')]

        return lanternfish(starting_fish, 80)


part = Part1()

part.add_result(5934, """
3,4,3,1,2
""")

part.add_result(380243)
