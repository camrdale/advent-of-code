import itertools
import string

from aoc.input import InputParser
from aoc.log import log, RESULT, INFO, DEBUG
from aoc.map import Coordinate, Offset, ParsedMap
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        map = ParsedMap(input, string.ascii_lowercase + string.ascii_uppercase + ''.join(str(i) for i in range(10)))

        log(DEBUG, map.width, map.height)
        log(DEBUG, map.features)

        antinodes: set[Coordinate] = set()
        for typednodes in map.features.values():
            for node1, node2 in itertools.combinations(typednodes, 2):
                offset: Offset = node2.difference(node1)
                antinode2 = node2.add(offset)
                if map.valid(antinode2):
                    log(DEBUG, node1, node2, antinode2)
                    antinodes.add(antinode2)
                antinode1 = node1.add(offset.negate())
                if map.valid(antinode1):
                    log(DEBUG, node2, node1, antinode1)
                    antinodes.add(antinode1)

        log(INFO, antinodes)

        unique_antinodes = len(antinodes)
        log(RESULT, 'Unique antinode locations:', unique_antinodes)
        return unique_antinodes


part = Part1()

part.add_result(14, """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""")

part.add_result(398)
