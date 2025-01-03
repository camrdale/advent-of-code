from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part

from .shared import PartNumberMap


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        map = PartNumberMap(input)

        part_numbers = map.part_number_locations()
        sum_part_numbers = 0
        while len(part_numbers) > 0:
            part_number = next(iter(part_numbers))
            full_part_number, used_part_numbers = map.get_part_number(part_number)
            part_numbers -= used_part_numbers
            sum_part_numbers += full_part_number

        log(RESULT, f'The sum of all the part numbers: {sum_part_numbers}')
        return sum_part_numbers


part = Part1()

part.add_result(4361, """
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

part.add_result(538046)
