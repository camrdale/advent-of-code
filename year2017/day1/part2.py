from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()[0]

        sum_matching_digits = sum(
            int(input[i])
            for i in range(len(input))
            if input[i] == input[(i + len(input) // 2) % len(input)])

        log.log(log.RESULT, f'The captcha solution is: {sum_matching_digits}')
        return sum_matching_digits


part = Part2()

part.add_result(6, """
1212
""")

part.add_result(0, """
1221
""")

part.add_result(4, """
123425
""")

part.add_result(12, """
123123
""")

part.add_result(4, """
12131415
""")

part.add_result(1080)
