from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2021.day12.shared import CaveMap


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        map = CaveMap(parser.get_input())

        num_paths = map.num_paths('start', 'end', one_small_cave_twice=True)

        log.log(log.RESULT, 'Number of unique paths through the cave system:', num_paths)
        return num_paths


part = Part2()

part.add_result(36, """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""")

part.add_result(103, """
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
""")

part.add_result(3509, """
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
""")

part.add_result(153592)
