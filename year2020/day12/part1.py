from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate, Direction, UP, DOWN, LEFT, RIGHT
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        direction = Direction.EAST
        location = Coordinate(0, 0)
        for line in input:
            match line[0], int(line[1:]):
                case 'N', value:
                    location = location.add(UP.times(value))
                case 'S', value:
                    location = location.add(DOWN.times(value))
                case 'E', value:
                    location = location.add(RIGHT.times(value))
                case 'W', value:
                    location = location.add(LEFT.times(value))
                case 'L', degrees:
                    assert degrees % 90 == 0, line
                    for _ in range(degrees // 90):
                        direction = direction.left()
                case 'R', degrees:
                    assert degrees % 90 == 0, line
                    for _ in range(degrees // 90):
                        direction = direction.right()
                case 'F', value:
                    location = location.add(direction.offset().times(value))
                case _:
                    raise ValueError(f'Unparseable: {line}')

        distance = location.difference(Coordinate(0, 0)).manhattan_distance()
        log.log(log.RESULT, f'The ship travels to {location}, a distance of: {distance}')
        return distance


part = Part1()

part.add_result(25, """
F10
N3
F7
R90
F11
""")

part.add_result(1424)
