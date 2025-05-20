from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2021.day20.shared import ImageEnhancer


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        enhancement_input, image_input = parser.get_two_part_input()

        enhancer = ImageEnhancer(enhancement_input[0], image_input)

        for _ in range(50):
            enhancer.enhance()
        log.log(log.INFO, enhancer.print_map())

        lit_pixels = enhancer.lit_pixels()
        log.log(log.RESULT, f'After 50 enhancements there are {lit_pixels} lit pixels')
        return lit_pixels


part = Part2()

part.add_result(3351, """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
""")

part.add_result(18509)
