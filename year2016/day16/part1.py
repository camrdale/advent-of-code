from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day16.shared import dragon_curve, dragon_checksum


class Part1(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()
        size: int = parser.get_additional_params()[0]

        data = list(map(int, input[0]))
        dragon_curve(size, data)
        checksum = ''.join(map(str, dragon_checksum(data)))

        log.log(log.RESULT, f'The checksum is: {checksum}')
        return checksum


part = Part1()

part.add_result('01100', """
10000
""", 20)

part.add_result('10100011010101011', """
11100010111110100
""", 272)
