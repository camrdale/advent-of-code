from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day23.shared import ElfMap


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        estimated_iterations = parser.get_additional_params()[0]

        elf_map = ElfMap(input)

        with log.ProgressBar(estimated_iterations=estimated_iterations, desc=f'day 22,2') as progress_bar:
            while elf_map.execute_round():
                log.log(log.DEBUG, f'== End of Round {elf_map.round_num} ==')
                log.log(log.DEBUG, elf_map.print_map())
                progress_bar.update()

        log.log(log.RESULT, f'No elf moves in round: {elf_map.round_num}')
        return elf_map.round_num


part = Part2()

part.add_result(20, r"""
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
""", 20)

part.add_result(986, None, 986)
