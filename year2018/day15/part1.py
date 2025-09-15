from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day15.shared import CaveMap


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        cave_map = CaveMap(input)

        cave_map.combat()

        cave_map.units.sort()
        log.log(log.INFO, cave_map.print_map(), cave_map.units)

        outcome = cave_map.outcome()

        log.log(log.RESULT, f'The result of the combat after {cave_map.rounds} completed rounds: {outcome}')
        return outcome


part = Part1()

part.add_result(27730, """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
""")

part.add_result(36334, """
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
""")

part.add_result(39514, """
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
""")

part.add_result(27755, """
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
""")

part.add_result(28944, """
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
""")

part.add_result(18740, """
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
""")

part.add_result(227290)
