from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate3D, NEIGHBORS_3D
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        cubes: set[Coordinate3D] = set()
        for line in input:
            cubes.add(Coordinate3D.from_text(line))

        surface_area = 0
        for cube in cubes:
            for neighbor in NEIGHBORS_3D:
                if cube.add(neighbor) not in cubes:
                    surface_area += 1

        log.log(log.RESULT, f'The surface area of the droplet is: {surface_area}')
        return surface_area


part = Part1()

part.add_result(10, r"""
1,1,1
2,1,1
""")

part.add_result(64, r"""
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
""")

part.add_result(4244)
