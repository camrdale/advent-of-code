from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate, Direction
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        location = Coordinate(0, 0)
        direction = Direction.NORTH
        for instruction in input[0].split(', '):
            if instruction[0] == 'R':
                direction = direction.right()
            else:
                direction = direction.left()

            location = location.add(direction.offset().times(int(instruction[1:])))

        distance = location.difference(Coordinate(0, 0)).manhattan_distance()
        log.log(log.RESULT, f'The Easter Bunny HQ is {distance} blocks away')
        return distance


part = Part1()

part.add_result(5, """
R2, L3
""")

part.add_result(2, """
R2, R2, R2
""")

part.add_result(12, """
R5, L5, R5, R3
""")

part.add_result(300)
