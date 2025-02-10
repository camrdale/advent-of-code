import collections
import itertools

import aoc.input
from aoc import log
import aoc.map
from aoc import runner

from year2019.day10 import shared


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()

        asteroid_map = aoc.map.ParsedMap(input, '#')
        asteroids = asteroid_map.features['#']

        visible: dict[aoc.map.Coordinate, set[shared.NormalizedDirection]] = collections.defaultdict(set)
        for asteroid1, asteroid2 in itertools.combinations(asteroids, 2):
            direction = shared.NormalizedDirection.from_offset(asteroid2.difference(asteroid1))
            visible[asteroid1].add(direction)
            visible[asteroid2].add(direction.negate())

        most_visible = max([(len(can_see), asteroid) for asteroid, can_see in visible.items()])
        log.log(log.DEBUG, sorted(visible[most_visible[1]]))
        log.log(log.RESULT, f'The most visible asteroid can see {most_visible[0]} at: {most_visible[1]}')
        return most_visible[0]


part = Part1()

part.add_result(8, r"""
.#..#
.....
#####
....#
...##
""")

part.add_result(33, r"""
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
""")

part.add_result(35, r"""
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
""")

part.add_result(41, r"""
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
""")

part.add_result(210, r"""
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
""")

part.add_result(253)
