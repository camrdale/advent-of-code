import itertools

from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        tiles = [Coordinate.from_text(line) for line in input]

        max_area = 0
        for tile_a, tile_b in itertools.combinations(tiles, 2):
            area = (abs(tile_a.x - tile_b.x) + 1) * (abs(tile_a.y - tile_b.y) + 1)
            if area > max_area:
                max_area = area

        log.log(log.RESULT, f'The largest area rectangle is: {max_area}')
        return max_area


part = Part1()

part.add_result(50, """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
""")

part.add_result(4737096935)
