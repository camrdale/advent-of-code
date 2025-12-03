from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        total_joltage = 0
        for line in input:
            joltages = list(map(int, line))
            first_digit = max(joltages[:-1])
            i = joltages.index(first_digit)
            second_digit = max(joltages[i+1:])
            joltage = first_digit * 10 + second_digit
            total_joltage += joltage

        log.log(log.RESULT, f'The total output joltage: {total_joltage}')
        return total_joltage


part = Part1()

part.add_result(357, """
987654321111111
811111111111119
234234234234278
818181911112111
""")

part.add_result(17244)
