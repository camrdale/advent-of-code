from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day10.shared import BalanceBots


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        balance_bots = BalanceBots(input)

        result = balance_bots.run()

        log.log(log.RESULT, f'The multiply of the output values: {result}')
        return result


part = Part2()

part.add_result(2666)
