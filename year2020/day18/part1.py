from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day18.shared import Expression


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        sum_results = 0
        for line in input:
            result, remaining = Expression.parse(line)
            assert len(remaining) == 0, remaining
            sum_results += result.value()

        log.log(log.RESULT, f'The sum of the evaluation of each expression: {sum_results}')
        return sum_results


part = Part1()

part.add_result(71, """
1 + 2 * 3 + 4 * 5 + 6
""")

part.add_result(51, """
1 + (2 * 3) + (4 * (5 + 6))
""")

part.add_result(26, """
2 * 3 + (4 * 5)
""")

part.add_result(437, """
5 + (8 * 3 + 9 + 3 * 4 * 3)
""")

part.add_result(12240, """
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
""")

part.add_result(13632, """
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
""")

part.add_result(67800526776934)
