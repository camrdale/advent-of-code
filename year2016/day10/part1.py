from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day10.shared import BalanceBots


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        stop_condition = int(parser.get_additional_params()[0]), int(parser.get_additional_params()[1])

        balance_bots = BalanceBots(input)

        result = balance_bots.run(stop_condition=stop_condition)

        log.log(log.RESULT, f'The bot that compares values {stop_condition}: {result}')
        return result


part = Part1()

part.add_result(2, """
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
""", 5, 2)

part.add_result(47, None, 61, 17)
