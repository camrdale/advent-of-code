from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate, Offset, UP, DOWN, LEFT, RIGHT
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        waypoint = UP.add(RIGHT.times(10))
        location = Coordinate(0, 0)
        for line in input:
            match line[0], int(line[1:]):
                case 'N', value:
                    waypoint = waypoint.add(UP.times(value))
                case 'S', value:
                    waypoint = waypoint.add(DOWN.times(value))
                case 'E', value:
                    waypoint = waypoint.add(RIGHT.times(value))
                case 'W', value:
                    waypoint = waypoint.add(LEFT.times(value))
                case 'L', degrees:
                    assert degrees % 90 == 0, line
                    for _ in range(degrees // 90):
                        waypoint = Offset(waypoint.y, -waypoint.x)
                case 'R', degrees:
                    assert degrees % 90 == 0, line
                    for _ in range(degrees // 90):
                        waypoint = Offset(-waypoint.y, waypoint.x)
                case 'F', value:
                    location = location.add(waypoint.times(value))
                case _:
                    raise ValueError(f'Unparseable: {line}')

        distance = location.difference(Coordinate(0, 0)).manhattan_distance()
        log.log(log.RESULT, f'The ship travels to {location}, a distance of: {distance}')
        return distance


part = Part2()

part.add_result(286, """
F10
N3
F7
R90
F11
""")

part.add_result(63447)
