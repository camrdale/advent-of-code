from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day12.shared import DisjointSet


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        disjoint_set = DisjointSet(input)

        zero_root = disjoint_set.find(0)

        log.log(log.RESULT, f'The group that contains the 0 program has size: {zero_root.size}')
        return zero_root.size


part = Part1()

part.add_result(6, """
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
""")

part.add_result(145)
