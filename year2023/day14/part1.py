from aoc.input import InputParser
from aoc.log import log, RESULT, DEBUG
from aoc.map import ParsedMap, Offset
from aoc.runner import Part

ROUNDED = 'O'
CUBE = '#'
NORTH = Offset(0, -1)


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        map = ParsedMap(parser.get_input(), ROUNDED + CUBE)

        rounded_rocks = sorted(map.features[ROUNDED])
        for rock in rounded_rocks:
            map.features[ROUNDED].remove(rock)
            while True:
                moved_rock = rock.add(NORTH)
                if map.valid(moved_rock) and moved_rock not in map.features[ROUNDED] and moved_rock not in map.features[CUBE]:
                    rock = moved_rock
                else:
                    break
            map.features[ROUNDED].add(rock)
        log(DEBUG, map.print_map())

        total_load = 0
        for rock in map.features[ROUNDED]:
            total_load += map.max_y + 1 - rock.y

        log(RESULT, f'Total load on the north support beams: {total_load}')
        return total_load


part = Part1()

part.add_result(136, """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
""")

part.add_result(113424)
