import itertools
import string

from aoc.input import InputParser
from aoc.log import log, RESULT, INFO, DEBUG
from aoc.map import Coordinate, Offset, ParsedMap
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        map = ParsedMap(input, string.ascii_lowercase + string.ascii_uppercase + ''.join(str(i) for i in range(10)))

        log(DEBUG, map.width, map.height)
        log(DEBUG, map.features)

        antinodes: set[Coordinate] = set()
        for typednodes in map.features.values():
            for node1, node2 in itertools.combinations(typednodes, 2):
                antinodes.add(node2)

                offset: Offset = node2.difference(node1)
                antinode = node2.add(offset)
                while map.valid(antinode):
                    log(DEBUG, node1, node2, antinode)
                    antinodes.add(antinode)
                    antinode = antinode.add(offset)

                offset = offset.negate()
                antinode = node2.add(offset)
                while map.valid(antinode):
                    log(DEBUG, node1, node2, antinode)
                    antinodes.add(antinode)
                    antinode = antinode.add(offset)

        log(INFO, antinodes)

        unique_antinodes = len(antinodes)
        log(RESULT, 'Unique antinode locations:', unique_antinodes)
        return unique_antinodes

part = Part2()

part.add_result(9, """
T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........
""")

part.add_result(34, """
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

part.add_result(1333)
