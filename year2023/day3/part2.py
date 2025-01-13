from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part

from .shared import PartNumberMap


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        map = PartNumberMap(input)

        gear_part_numbers = map.get_gears()
        sum_gear_ratios = sum(gear_num[0]*gear_num[1] for gear_num in gear_part_numbers)
        log(RESULT, f'The sum of all the gear ratios: {sum_gear_ratios}')
        return sum_gear_ratios


part = Part2()

part.add_result(467835, """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""")

part.add_result(81709807)
