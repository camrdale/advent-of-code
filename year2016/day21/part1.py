from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day21.shared import apply_operation


class Part1(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()
        password = parser.get_additional_params()[0]

        scram: list[str] = list(password)
        for line in input:
            apply_operation(line, scram)
            log.log(log.INFO, scram)

        scrambled_password = ''.join(scram)
        log.log(log.RESULT, f'The pasword "{password}" scrambled becomes: "{scrambled_password}"')
        return scrambled_password


part = Part1()

part.add_result('decab', """
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d
""", 'abcde')

part.add_result('dgfaehcb', None, 'abcdefgh')
