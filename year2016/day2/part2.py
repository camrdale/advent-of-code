from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day2.shared import code_finder


KEYPAD = """
  1
 234
56789
 ABC
  D
"""


class Part2(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()

        code = code_finder(input, KEYPAD, '5')

        log.log(log.RESULT, f'The bathroom code is "{code}"')
        return code


part = Part2()

part.add_result('5DB3', """
ULL
RRDDD
LURDL
UUUUD
""")

part.add_result('27CA4')
