from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day9.shared import xmas_invalid


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        preamble: int = parser.get_additional_params()[0]

        data = list(map(int, input))
        invalid = xmas_invalid(data, preamble)

        log.log(log.RESULT, f'The first invalid value: {invalid}')
        return invalid


part = Part1()

part.add_result(127, """
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
""", 5)

part.add_result(36845998, None, 25)
