import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


NUMBERS = re.compile(r'-?[0-9]+')


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        total = 0
        for number in NUMBERS.findall(input[0]):
            try:
                total += int(number)
            except ValueError:
                pass

        log.log(log.RESULT, f'The sum of all numbers: {total}')
        return total


part = Part1()

part.add_result(6, """
[1,2,3]
""")

part.add_result(6, """
{"a":2,"b":4}
""")

part.add_result(3, """
[[[3]]]
""")

part.add_result(3, """
{"a":{"b":4},"c":-1}
""")

part.add_result(0, """
{"a":[-1,1]}
""")

part.add_result(0, """
[-1,{"a":1}]
""")

part.add_result(0, """
[]
""")

part.add_result(0, """
{}
""")

part.add_result(111754)
