from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day12.shared import DisjointSet


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        disjoint_set = DisjointSet(input)

        num_groups = sum(node.parent == node for node in disjoint_set.nodes)

        log.log(log.RESULT, f'The number of groups of programs: {num_groups}')
        return num_groups


part = Part2()

part.add_result(2, """
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
""")

part.add_result(207)
