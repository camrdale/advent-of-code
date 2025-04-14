from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate, Offset, NEIGHBORS, DIAGONAL_NEIGHBORS, UP, DOWN, LEFT, RIGHT
from aoc.runner import Part


WITHIN_ONE = set(NEIGHBORS + DIAGONAL_NEIGHBORS + [Offset(0,0)])

DIRECTIONS = {'U': UP, 'R': RIGHT, 'D': DOWN, 'L': LEFT}


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        knots = [Coordinate(0,0)]*10
        visited = set([knots[9]])
        for line in input:
            direction = DIRECTIONS[line.split()[0]]
            length = int(line.split()[1])
            for _ in range(length):
                knots[0] = knots[0].add(direction)
                for knot in range(1, 10):
                    to_knot_ahead = knots[knot-1].difference(knots[knot])
                    if to_knot_ahead not in WITHIN_ONE:
                        knots[knot] = knots[knot].add(to_knot_ahead.to_direction())
                        if knot == 9:
                            visited.add(knots[9])

        log.log(log.RESULT, f'The number of positions visited by the tail: {len(visited)}')
        return len(visited)


part = Part2()

part.add_result(1, r"""
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""")

part.add_result(36, r"""
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
""")

part.add_result(2531)
