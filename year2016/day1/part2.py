from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate, Direction
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        location = Coordinate(0, 0)
        direction = Direction.NORTH
        visited: set[Coordinate] = set([location])
        for instruction in input[0].split(', '):
            if instruction[0] == 'R':
                direction = direction.right()
            else:
                direction = direction.left()

            for _ in range(int(instruction[1:])):
                location = location.add(direction.offset())

                if location in visited:
                    distance = location.difference(Coordinate(0, 0)).manhattan_distance()
                    log.log(log.RESULT, f'The first location visited twice is {distance} blocks away')
                    return distance
                visited.add(location)

        raise ValueError(f'Failed to find a location that is visited twice.')


part = Part1()

part.add_result(4, """
R8, R4, R4, R8
""")

part.add_result(159)
