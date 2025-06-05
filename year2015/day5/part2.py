import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


DOUBLE_PAIR = re.compile(r'(..).*\1')
REPEAT_WITH_BETWEEN = re.compile(r'(.).\1')


def nice(string: str) -> bool:
    if DOUBLE_PAIR.search(string) is None:
        return False
    if REPEAT_WITH_BETWEEN.search(string) is None:
        return False
    return True


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        num_nice = 0
        for line in input:
            if nice(line):
                num_nice += 1

        log.log(log.RESULT, f'The number of nice strings: {num_nice}')
        return num_nice


part = Part2()

part.add_result(1, """
qjhvhtzxzqqjkmpb
""")

part.add_result(1, """
xxyxx
""")

part.add_result(0, """
uurcxstgmygtbstg
""")

part.add_result(0, """
ieodomkazucvgmuy
""")

part.add_result(69)
