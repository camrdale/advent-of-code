from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate, Offset, NEIGHBORS, DIAGONAL_NEIGHBORS, UP, DOWN, LEFT, RIGHT
from aoc.runner import Part


WITHIN_ONE = set(NEIGHBORS + DIAGONAL_NEIGHBORS + [Offset(0,0)])

DIRECTIONS = {'U': UP, 'R': RIGHT, 'D': DOWN, 'L': LEFT}


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        head = Coordinate(0,0)
        tail = head
        visited = set([tail])
        for line in input:
            direction = DIRECTIONS[line.split()[0]]
            length = int(line.split()[1])
            for _ in range(length):
                head = head.add(direction)
                to_head = head.difference(tail)
                if to_head not in WITHIN_ONE:
                    tail = tail.add(to_head.to_direction())
                    visited.add(tail)

        log.log(log.RESULT, f'The number of positions visited by the tail: {len(visited)}')
        return len(visited)


part = Part1()

part.add_result(13, r"""
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""")

part.add_result(6498)
