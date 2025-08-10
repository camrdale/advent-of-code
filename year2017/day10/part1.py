from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day10.shared import knot_hash


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        lengths = list(map(int, parser.get_input()[0].split(',')))
        list_size: int = parser.get_additional_params()[0]

        l = knot_hash(lengths, list_size=list_size)

        log.log(log.RESULT, f'The first 2 numbers in the list {l[0]} * {l[1]} = {l[0]*l[1]}')
        return l[0]*l[1]


part = Part1()

part.add_result(12, """
3,4,1,5
""", 5)

part.add_result(2928, None, 256)
