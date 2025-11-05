from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day5.shared import from_binary_space


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        max_seat_id = max(from_binary_space(line) for line in input)

        log.log(log.RESULT, f'The highest seat ID on a boarding pass: {max_seat_id}')
        return max_seat_id


part = Part1()

part.add_result(357, """
FBFBBFFRLR
""")

part.add_result(567, """
BFFFBBFRRR
""")

part.add_result(119, """
FFFBBBFRRR
""")

part.add_result(820, """
BBFFBBFRLL
""")

part.add_result(994)
