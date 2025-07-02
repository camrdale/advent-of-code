from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day2.shared import code_finder


KEYPAD = """
123
456
789
"""


class Part1(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()

        code = code_finder(input, KEYPAD, '5')

        log.log(log.RESULT, f'The bathroom code is "{code}"')
        return code


part = Part1()

part.add_result('1985', """
ULL
RRDDD
LURDL
UUUUD
""")

part.add_result('45973')
