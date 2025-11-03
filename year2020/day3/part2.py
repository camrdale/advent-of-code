from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day3.shared import TobogganMap, Offset


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        toboggan_map = TobogganMap(input)

        tree_multiple = 1
        for x in range(1, 9, 2):
            tree_multiple *= len(toboggan_map.path(Offset(x, 1)))
        tree_multiple *= len(toboggan_map.path(Offset(1, 2)))

        log.log(log.RESULT, f'The product of the number of trees encountered: {tree_multiple}')
        return tree_multiple


part = Part2()

part.add_result(336, """
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

part.add_result(6419669520)
