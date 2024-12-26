from aoc.input import InputParser
from aoc.runner import Part

from .shared import vents


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        return vents(input, False)


part = Part1()

part.add_result(5, """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""")

part.add_result(5576)
