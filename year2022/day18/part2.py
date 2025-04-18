from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate3D, Coordinate, NEIGHBORS_3D
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        min_x, min_y, min_z = 10000,10000,10000
        max_x, max_y, max_z = -1,-1,-1
        cubes: set[Coordinate3D] = set()
        for line in input:
            cube = Coordinate3D.from_text(line)
            cubes.add(cube)
            if cube.location.x > max_x:
                max_x = cube.location.x
            if cube.location.y > max_y:
                max_y = cube.location.y
            if cube.z > max_z:
                max_z = cube.z
            if cube.location.x < min_x:
                min_x = cube.location.x
            if cube.location.y < min_y:
                min_y = cube.location.y
            if cube.z < min_z:
                min_z = cube.z

        log.log(log.INFO, f'The droplet extends from x={min_x}-{max_x}, y={min_y}-{max_y}, z={min_z}-{max_z}')

        surface_area: set[tuple[Coordinate3D, Coordinate3D]] = set()
        visited: set[Coordinate3D] = set()
        to_check: list[Coordinate3D] = [Coordinate3D(min_z-1, Coordinate(min_x-1, min_y-1))]
        while to_check:
            location = to_check.pop()
            if location in visited:
                continue
            visited.add(location)
            for neighbor in [location.add(offset) for offset in NEIGHBORS_3D]:
                if neighbor.z < min_z-1 or neighbor.location.x < min_x-1 or neighbor.location.y < min_y-1 or neighbor.z > max_z+1 or neighbor.location.x > max_x+1 or neighbor.location.y > max_y+1:
                    continue
                if neighbor in cubes:
                    surface_area.add((location, neighbor))
                else:
                    to_check.append(neighbor)

        log.log(log.RESULT, f'The exterior surface area of the droplet is: {len(surface_area)}')
        return len(surface_area)


part = Part2()

part.add_result(10, r"""
1,1,1
2,1,1
""")

part.add_result(58, r"""
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

part.add_result(2460)
