from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate, Direction, NEIGHBORS, DIAGONAL_NEIGHBORS
from aoc.runner import Part


ALL_NEIGHBORS = NEIGHBORS + DIAGONAL_NEIGHBORS


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        target = int(input[0])

        direction = Direction.SOUTH
        location = Coordinate(0, 0)
        visited = {location: 1}
        adjacent_sum = 1
        while adjacent_sum <= target:
            if location.add(direction.left().offset()) not in visited:
                direction = direction.left()
            location = location.add(direction.offset())
            adjacent_sum = sum(visited.get(location.add(neighbor), 0) for neighbor in ALL_NEIGHBORS)
            visited[location] = adjacent_sum
            log.log(log.INFO, f'{location}: {adjacent_sum}')

        log.log(log.RESULT, f'The first value larger than the target: {adjacent_sum}')
        return adjacent_sum


part = Part2()

part.add_result(304, """
200
""")

part.add_result(806, """
750
""")

part.add_result(312453, """
312051
""")
