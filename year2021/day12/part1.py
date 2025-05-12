from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2021.day12.shared import CaveMap


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        map = CaveMap(parser.get_input())

        num_paths = map.num_paths('start', 'end')

        log.log(log.RESULT, 'Number of unique paths through the cave system:', num_paths)
        return num_paths


part = Part1()

part.add_result(10, """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""")

part.add_result(19, """
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

part.add_result(226, """
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

part.add_result(5874)
