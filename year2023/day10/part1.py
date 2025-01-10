from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part

from year2023.day10.shared import PipeMap


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        map = PipeMap(parser)

        steps = len(map.loop_nodes()) // 2
        log(RESULT, f'Steps to the farthest position: {steps}')
        return steps


part = Part1()

part.add_result(4, """
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
""")

part.add_result(8, """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
""")

part.add_result(6968)
