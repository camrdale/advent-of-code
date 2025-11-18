from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day18.shared import Expression


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        sum_results = 0
        for line in input:
            result, remaining = Expression.parse(line, add_first=True)
            assert len(remaining) == 0, remaining
            sum_results += result.value()

        log.log(log.RESULT, f'The sum of the evaluation of each expression: {sum_results}')
        return sum_results


part = Part2()

part.add_result(231, """
1 + 2 * 3 + 4 * 5 + 6
""")

part.add_result(51, """
1 + (2 * 3) + (4 * (5 + 6))
""")

part.add_result(46, """
2 * 3 + (4 * 5)
""")

part.add_result(1445, """
5 + (8 * 3 + 9 + 3 * 4 * 3)
""")

part.add_result(669060, """
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
""")

part.add_result(23340, """
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
""")

part.add_result(340789638435483)
