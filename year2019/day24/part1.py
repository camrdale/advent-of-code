from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2019.day24.shared import parse_and_build_bit_masks, to_map


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        biodiversity, bit_masks = parse_and_build_bit_masks(input)

        print_map = '\n'.join(to_map(biodiversity)) + '\n'
        log.log(log.INFO, f'{print_map}')

        found_biodiversities: set[int] = set()
        while biodiversity not in found_biodiversities:
            found_biodiversities.add(biodiversity)
            new_biodiversity = biodiversity
            for i in range(25):
                bit_mask = bit_masks[i]
                num_adjacent = (biodiversity & bit_mask.adjacent_mask).bit_count()
                if biodiversity & bit_mask.bit_mask:
                    if num_adjacent != 1:
                        new_biodiversity ^= bit_mask.bit_mask
                else:
                    if num_adjacent == 1 or num_adjacent == 2:
                        new_biodiversity ^= bit_mask.bit_mask
            biodiversity = new_biodiversity
            print_map = '\n'.join(to_map(biodiversity)) + '\n'
            log.log(log.DEBUG, f'{print_map}')

        log.log(log.RESULT, f'First repeated biodiversity: {biodiversity}')

        return biodiversity


part = Part1()

part.add_result(2129920, r"""
....#
#..#.
#..##
..#..
#....
""")

part.add_result(27777901)
