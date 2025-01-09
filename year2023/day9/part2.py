import itertools

from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        sum_new_elements = 0
        for line in input:
            history = list(map(int, line.split()))
            sum_first_elements = 0
            sign = -1
            while any(history):
                sum_first_elements = history[0] - sum_first_elements
                sign = sign * -1
                history = [e2 - e1 for e1, e2 in itertools.pairwise(history)]
            log(INFO, f'{sum_first_elements} {sign}')
            sum_new_elements += sign * sum_first_elements

        log(RESULT, f'The sum of the extrapolated vales: {sum_new_elements}')
        return sum_new_elements


part = Part2()

part.add_result(2, """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
""")

part.add_result(975)
