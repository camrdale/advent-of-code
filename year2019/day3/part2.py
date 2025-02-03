import aoc.input
from aoc import log
from aoc import runner

from year2019.day3 import shared


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()

        first_wire = shared.build_path_dict(input[0].split(','))
        second_wire = shared.build_path_dict(input[1].split(','))
        intersections = first_wire.keys() & second_wire.keys()
        steps = [first_wire[coord] + second_wire[coord] for coord in intersections]
        min_steps = min(steps)

        log.log(log.RESULT, f'Minimum number of combined steps to intersection: {min_steps}')
        return min_steps


part = Part1()

part.add_result(30, r"""
R8,U5,L5,D3
U7,R6,D4,L4
""")

part.add_result(610, r"""
R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83
""")

part.add_result(410, r"""
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7
""")

part.add_result(16524)
