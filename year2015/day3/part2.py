from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate, UP, DOWN, LEFT, RIGHT
from aoc.runner import Part


DIRECTIONS = {'^': UP, 'v': DOWN, '>': RIGHT, '<': LEFT}


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        santa_location = Coordinate(0,0)
        robot_location = Coordinate(0,0)
        visited = set([santa_location, robot_location])
        for i, direction in enumerate(input[0]):
            if i % 2 == 0:
                santa_location = santa_location.add(DIRECTIONS[direction])
                visited.add(santa_location)
            else:
                robot_location = robot_location.add(DIRECTIONS[direction])
                visited.add(robot_location)

        log.log(log.RESULT, f'Number of houses that receive at least one present: {len(visited)}')
        return len(visited)


part = Part2()

part.add_result(3, """
^v
""")

part.add_result(3, """
^>v<
""")

part.add_result(11, """
^v^v^v^v^v
""")

part.add_result(2639)
