from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day21.shared import apply_operation


class Part2(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()
        scrambled_password = parser.get_additional_params()[0]

        scram: list[str] = list(scrambled_password)
        for line in input[::-1]:
            apply_operation(line, scram, reverse=True)
            log.log(log.INFO, scram)

        password = ''.join(scram)
        log.log(log.RESULT, f'The scrambled pasword "{scrambled_password}" unscrambled becomes: "{password}"')
        return password


part = Part2()

part.add_result('abcde', """
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d
""", 'decab')

# From part 1
part.add_result('abcdefgh', None, 'dgfaehcb')

part.add_result('fdhgacbe', None, 'fbgdceah')
