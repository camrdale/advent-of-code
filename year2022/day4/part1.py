import re

from aoc.input import InputParser
from aoc import log
from aoc.range import Range
from aoc.runner import Part


ASSIGNMENTS = re.compile(r'([0-9]*)-([0-9]*),([0-9]*)-([0-9]*)')


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_parsed_int_input(ASSIGNMENTS)

        total_contained = 0
        for first_min, first_max, second_min, second_max in input:
            first = Range.closed(first_min, first_max)
            second = Range.closed(second_min, second_max)
            if first.contains(second) or second.contains(first):
                log.log(log.INFO, f'One assignment fully contains the other: {first_min}-{first_max}, {second_min}-{second_max}')
                total_contained += 1
        
        log.log(log.RESULT, f'The number of pairs where one fully contains the other: {total_contained}')
        return total_contained


part = Part1()

part.add_result(2, r"""
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""")

part.add_result(576)
