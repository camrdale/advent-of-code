from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day23.shared import Nanobot


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        nanobots: list[Nanobot] = []
        for line in input:
            nanobots.append(Nanobot.from_text(line))
        
        nanobots.sort()

        largest_radius = nanobots[-1]
        num_in_range = sum(largest_radius.in_range(nanobot.location) for nanobot in nanobots)

        log.log(log.RESULT, f'The number of nanobots in range of {largest_radius}: {num_in_range}')
        return num_in_range


part = Part1()

part.add_result(7, """
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
""")

part.add_result(232)
