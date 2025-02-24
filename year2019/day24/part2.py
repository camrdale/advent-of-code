import collections

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2019.day24.shared import parse_and_build_bit_masks, to_map


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        num_minutes: int = parser.get_additional_params()[0]

        biodiversity, bit_masks = parse_and_build_bit_masks(input)
        
        biodiversities: dict[int, int] = collections.defaultdict(int)
        biodiversities[0] = biodiversity
        max_level = 0
        min_level = 0
        for _ in range(num_minutes):
            new_biodiversities = biodiversities.copy()
            for level in range(min_level - 1, max_level + 2):
                for i in range(25):
                    if i == 12:
                        continue
                    bit_mask = bit_masks[i]
                    num_adjacent = (
                        (biodiversities[level] & bit_mask.adjacent_mask).bit_count()
                        + (biodiversities[level-1] & bit_mask.adjacent_mask_above).bit_count()
                        + (biodiversities[level+1] & bit_mask.adjacent_mask_below).bit_count()
                    )
                    if biodiversities[level] & bit_mask.bit_mask:
                        if num_adjacent != 1:
                            new_biodiversities[level] ^= bit_mask.bit_mask
                    else:
                        if num_adjacent == 1 or num_adjacent == 2:
                            new_biodiversities[level] ^= bit_mask.bit_mask
                if level < min_level and new_biodiversities[level] != 0:
                    min_level = level
                if level > max_level and new_biodiversities[level] != 0:
                    max_level = level
            biodiversities = new_biodiversities

        for level in range(min_level, max_level + 1):
            print_map = '\n'.join(to_map(biodiversities[level]))
            log.log(log.DEBUG, f'Depth {level}:\n{print_map}')

        num_bugs = sum([biodiversities[level].bit_count() for level in range(min_level, max_level + 1)])
        log.log(log.RESULT, f'After {num_minutes} minutes, there are {num_bugs} bugs')

        return num_bugs


part = Part2()

part.add_result(99, r"""
....#
#..#.
#..##
..#..
#....
""", 10)

part.add_result(2047, None, 200)
