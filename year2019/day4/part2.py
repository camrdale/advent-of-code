import aoc.input
from aoc import log
from aoc import runner


def valid_password(password: int) -> bool:
    digits = list(map(int, str(password)))
    adjacency_used = False
    for i in range(1, len(digits)):
        if digits[i-1] == digits[i] and (i-2 < 0 or digits[i-2] != digits[i]) and (i+1 >= len(digits) or digits[i+1] != digits[i]):
            adjacency_used = True
        if digits[i-1] > digits[i]:
            return False
    return adjacency_used


class Part2(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()

        starting_range, ending_range = map(int, input[0].split('-'))

        total_passwords = 0
        for password in range(starting_range+1, ending_range):
            if valid_password(password):
                total_passwords += 1

        log.log(log.RESULT, f'The number of different valid passwords: {total_passwords}')
        return total_passwords


part = Part2()

part.add_result(1253, r"""
138307-654504
""")
