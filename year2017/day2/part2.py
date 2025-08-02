import itertools

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        evenly_divisible = 0
        for line in input:
            nums = list(map(int, line.split()))
            for num1, num2 in itertools.permutations(nums, 2):
                if num1 % num2 == 0:
                    evenly_divisible += num1 // num2
                    break

        log.log(log.RESULT, f'The sum of the evenly divisible numbers in each row is: {evenly_divisible}')
        return evenly_divisible


part = Part1()

part.add_result(9, """
5 9 2 8
9 4 7 3
3 8 6 5
""")

part.add_result(236)
