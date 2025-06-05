import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


THREE_VOWELS = re.compile(r'[aeiou].*[aeiou].*[aeiou]')
DOUBLE_LETTER = re.compile(r'(.)\1')
NAUGHTY = re.compile(r'(ab|cd|pq|xy)')


def nice(string: str) -> bool:
    if THREE_VOWELS.search(string) is None:
        return False
    if DOUBLE_LETTER.search(string) is None:
        return False
    if NAUGHTY.search(string) is not None:
        return False
    return True


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        num_nice = 0
        for line in input:
            if nice(line):
                num_nice += 1

        log.log(log.RESULT, f'The number of nice strings: {num_nice}')
        return num_nice


part = Part1()

part.add_result(1, """
ugknbfddgicrmopn
""")

part.add_result(1, """
aaa
""")

part.add_result(0, """
jchzalrnumimnmhp
""")

part.add_result(0, """
haegwjzuvuyypxyu
""")

part.add_result(0, """
dvszwmarrgswjxmb
""")

part.add_result(238)
