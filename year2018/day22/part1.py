from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate
from aoc.runner import Part

from year2018.day22.shared import CaveMap


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        depth = int(input[0].split()[1])
        target = Coordinate.from_text(input[1].split()[1])

        cave_map = CaveMap(depth, target)

        risk_level = 0
        for y in range(target.y + 1):
            for x in range(target.x + 1):
                risk_level += cave_map.region_type(Coordinate(x,y))

        log.log(log.RESULT, f'The total risk level for the target square: {risk_level}')
        return risk_level


part = Part1()

part.add_result(114, """
depth: 510
target: 10,10
""")

part.add_result(7402)
