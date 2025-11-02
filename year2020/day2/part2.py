import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


PASSWORD = re.compile(r'([0-9]*)-([0-9]*) ([a-z]): ([a-z]*)')


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        valid = 0
        for line in input:
            match = PASSWORD.match(line)
            assert match is not None, line

            position1 = int(match.group(1)) - 1
            position2 = int(match.group(2)) - 1
            required_letter = match.group(3)
            password = match.group(4)

            if (password[position1] == required_letter) + (password[position2] == required_letter) == 1:
                valid += 1

        log.log(log.RESULT, f'The number of valid passwords: {valid}')
        return valid


part = Part2()

part.add_result(1, """
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
""")

part.add_result(584)
