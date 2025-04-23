from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day23.shared import ElfMap


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        elf_map = ElfMap(input)

        for round in range(10):
            elf_map.execute_round()
            log.log(log.DEBUG, f'== End of Round {round+1} ==')
            log.log(log.DEBUG, elf_map.print_map())

        empty_tiles = elf_map.empty_tiles()
        log.log(log.RESULT, f'After 10 rounds, the number of empty tiles: {empty_tiles}')
        return empty_tiles


part = Part1()

part.add_result(110, r"""
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
""")

part.add_result(4162)
