from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2025.day2.shared import ProductIdRange


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        ranges = ProductIdRange.from_input(input[0])

        sum_invalid = sum(range.sum_invalid(all_sequence_lengths=True) for range in ranges)

        log.log(log.RESULT, f'The sum of the invalid IDs in the product ranges: {sum_invalid}')
        return sum_invalid


part = Part1()

part.add_result(4174379265, """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
""")

part.add_result(43287141963)
