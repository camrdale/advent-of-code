import itertools

from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.map import ParsedMap, Offset
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        expansion_multiplier: int
        expansion_multiplier, = parser.get_additional_params()

        map = ParsedMap(input, '#')
        galaxies = map.features['#']

        galaxy_xs = {galaxy.x for galaxy in galaxies}
        galaxy_ys = {galaxy.y for galaxy in galaxies}

        delta_x: dict[int, int] = {}
        delta = 0
        for i in range(map.min_x, map.max_x + 1):
            if i not in galaxy_xs:
                delta += expansion_multiplier - 1
            delta_x[i] = delta

        delta_y: dict[int, int] = {}
        delta = 0
        for i in range(map.min_y, map.max_y + 1):
            if i not in galaxy_ys:
                delta += expansion_multiplier - 1
            delta_y[i] = delta

        expanded_galaxies = [
            galaxy.add(Offset(delta_x[galaxy.x], delta_y[galaxy.y]))
            for galaxy in galaxies]

        sum_path_lengths = 0
        for galaxy_1, galaxy_2 in itertools.combinations(expanded_galaxies, 2):
            offset = galaxy_1.difference(galaxy_2)
            sum_path_lengths += abs(offset.x) + abs(offset.y)

        log(RESULT, f'Sum of all the path lengths: {sum_path_lengths}')
        return sum_path_lengths


part = Part2()

part.add_result(1030, """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""", 10)

part.add_result(8410, """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""", 100)

part.add_result(699909023130, None, 1000000)
