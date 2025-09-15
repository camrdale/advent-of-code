import math

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day15.shared import CaveMap, HIT_POINTS


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        elf_power = 4
        while True:
            cave_map = CaveMap(input, elf_power=elf_power)

            complete = cave_map.combat(abort_on_elf_death=True)
            if complete:
                break

            num_hits = math.ceil(HIT_POINTS / elf_power)
            # Skip elf power levels that result in the same number of hits to kill
            while math.ceil(200 / elf_power) == num_hits:
                elf_power += 1
        
        cave_map.units.sort()
        log.log(log.INFO, cave_map.print_map(), cave_map.units)

        outcome = cave_map.outcome()

        log.log(log.RESULT, f'The elves all survive with attack power {elf_power}, after {cave_map.rounds} completed rounds, outcome: {outcome}')
        return outcome


part = Part2()

part.add_result(4988, """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
""")

part.add_result(31284, """
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
""")

part.add_result(3478, """
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
""")

part.add_result(6474, """
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
""")

part.add_result(1140, """
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

part.add_result(53725)
