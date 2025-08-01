import itertools

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()[0]

        sum_matching_digits = sum(
            int(a)
            for (a, b) in itertools.pairwise(input)
            if a == b)
        sum_matching_digits += int(input[0]) if input[0] == input[-1] else 0

        log.log(log.RESULT, f'The captcha solution is: {sum_matching_digits}')
        return sum_matching_digits


part = Part1()

part.add_result(3, """
1122
""")

part.add_result(4, """
1111
""")

part.add_result(0, """
1234
""")

part.add_result(9, """
91212129
""")

part.add_result(1031)
