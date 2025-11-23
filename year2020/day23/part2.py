from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

import itertools

from year2020.day23.shared import play_cups


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input_cups = list(map(int, parser.get_input()[0]))

        max_target = 1_000_000

        cups = [0] * (max_target + 1)
        for a,  b in itertools.pairwise(input_cups):
            cups[a] = b
        cups[input_cups[-1]] = 10
        for i in range(10, max_target):
            cups[i] = i + 1
        cups[max_target] = input_cups[0]

        play_cups(cups, input_cups[0], 10_000_000)

        result = cups[1] * cups[cups[1]]

        log.log(log.RESULT, f'The product of the two cups after 1 is: {result}')
        return result


part = Part2()

part.add_result(149245887792, '389125467')

part.add_result(11591415792, '318946572')
