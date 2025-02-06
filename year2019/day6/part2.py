import aoc.input
from aoc import log
from aoc import runner

from year2019.day6 import shared


class Part2(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()

        objects = shared.build_tree(input)
        
        num_hops = 0
        santa_orbits = objects['SAN']
        my_orbits = objects['YOU']
        while santa_orbits.depth > my_orbits.depth:
            santa_orbits = santa_orbits.orbits
            num_hops += 1
        while my_orbits.depth > santa_orbits.depth:
            my_orbits = my_orbits.orbits
            num_hops += 1
        while santa_orbits != my_orbits:
            santa_orbits = santa_orbits.orbits
            my_orbits = my_orbits.orbits
            num_hops += 2
        
        log.log(log.RESULT, f'Total number of orbital transfers reuqired: {num_hops - 2}')
        return num_hops - 2


part = Part2()

part.add_result(4, r"""
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
K)YOU
I)SAN
""")

part.add_result(412)
