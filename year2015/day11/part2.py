from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2015.day11.shared import next_password


class Part2(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()

        password = next_password(next_password(input[0]))

        log.log(log.RESULT, f'The NEXT next valid password: {password}')
        return password


part = Part2()

part.add_result('vzcaabcc', 'vzbxkghb')
