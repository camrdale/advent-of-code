import aoc.input
from aoc import log
from aoc import runner

from year2019.day6 import shared


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()

        objects = shared.build_tree(input)

        total_depth = sum(orbital_object.depth for orbital_object in objects.values())
        
        log.log(log.RESULT, f'Total number of direct and indirect orbits: {total_depth}')
        return total_depth


part = Part1()

part.add_result(42, r"""
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
""")

part.add_result(186597)
