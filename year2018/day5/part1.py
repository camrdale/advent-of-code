from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day5.shared import react


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()[0]

        polymer = react(input)

        log.log(log.RESULT, f'The number of polymer units remaining: {len(polymer)}')
        return len(polymer)


part = Part1()

part.add_result(10, """
dabAcCaCBAcCcaDA
""")

part.add_result(11540)
