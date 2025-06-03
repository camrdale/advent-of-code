from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate, UP, DOWN, LEFT, RIGHT
from aoc.runner import Part


DIRECTIONS = {'^': UP, 'v': DOWN, '>': RIGHT, '<': LEFT}


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        location = Coordinate(0,0)
        visited = set([location])
        for direction in input[0]:
            location = location.add(DIRECTIONS[direction])
            visited.add(location)

        log.log(log.RESULT, f'Number of houses that receive at least one present: {len(visited)}')
        return len(visited)


part = Part1()

part.add_result(2, """
>
""")

part.add_result(4, """
^>v<
""")

part.add_result(2, """
^v^v^v^v^v
""")

part.add_result(2565)
