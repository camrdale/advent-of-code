from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate
from aoc.runner import Part

from year2018.day22.shared import CaveMap


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        depth = int(input[0].split()[1])
        target = Coordinate.from_text(input[1].split()[1])

        cave_map = CaveMap(depth, target)

        shortest_path = cave_map.shortest_cave_route()

        log.log(log.RESULT, f'The shortest time to reach the target: {shortest_path.length}')
        return shortest_path.length


part = Part2()

part.add_result(45, """
depth: 510
target: 10,10
""")

part.add_result(1025)
