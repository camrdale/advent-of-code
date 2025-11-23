from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

import itertools

from year2020.day23.shared import play_cups


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input_cups = list(map(int, parser.get_input()[0]))

        max_target = 9
        cups = [0] * (max_target + 1)
        for a, b in itertools.pairwise(input_cups):
            cups[a] = b
        cups[input_cups[-1]] = input_cups[0]

        play_cups(cups, input_cups[0], 100)

        next = 1
        result = ''
        while cups[next] != 1:
            next = cups[next]
            result += str(next)

        log.log(log.RESULT, f'The labels of the cups after 1 are: {result}')
        return int(result)


part = Part1()

part.add_result(67384529, '389125467')

part.add_result(52864379, '318946572')
