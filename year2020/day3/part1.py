from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day3.shared import TobogganMap, Offset


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        toboggan_map = TobogganMap(input)

        trees = toboggan_map.path(Offset(3, 1))

        log.log(log.RESULT, f'The number of trees encountered: {len(trees)}')
        return len(trees)


part = Part1()

part.add_result(7, """
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
""")

part.add_result(159)
