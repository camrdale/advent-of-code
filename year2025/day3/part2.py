from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        total_joltage = 0
        for line in input:
            joltages = list(map(int, line))
            joltage = 0
            start = 0
            for i in range(11, -1, -1):
                possible_joltages = joltages[start:(-i if i > 0 else None)]
                max_digit = max(possible_joltages)
                joltage += (10**i) * max_digit
                start += possible_joltages.index(max_digit) + 1
            total_joltage += joltage

        log.log(log.RESULT, f'The total output joltage: {total_joltage}')
        return total_joltage


part = Part2()

part.add_result(3121910778619, """
987654321111111
811111111111119
234234234234278
818181911112111
""")

part.add_result(171435596092638)
