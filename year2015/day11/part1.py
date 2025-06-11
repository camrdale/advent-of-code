from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2015.day11.shared import next_password


class Part1(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()

        password = next_password(input[0])

        log.log(log.RESULT, f'The next valid password: {password}')
        return password


part = Part1()

part.add_result('abcdffaa', 'abcdefgh')

part.add_result('ghjaabcc', 'ghijklmn')

part.add_result('vzbxxyzz', 'vzbxkghb')
