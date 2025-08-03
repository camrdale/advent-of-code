from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate, Direction
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        square = int(input[0])

        i = 1
        direction = Direction.SOUTH
        location = Coordinate(0, 0)
        visited = set([location])
        while i != square:
            if location.add(direction.left().offset()) not in visited:
                direction = direction.left()
            location = location.add(direction.offset())
            visited.add(location)
            i += 1

        distance = location.difference(Coordinate(0, 0)).manhattan_distance()
        log.log(log.RESULT, f'The steps to carry the data to the origin: {distance}')
        return distance


part = Part1()

part.add_result(0, """
1
""")

part.add_result(3, """
12
""")

part.add_result(2, """
23
""")

part.add_result(31, """
1024
""")

part.add_result(430, """
312051
""")
