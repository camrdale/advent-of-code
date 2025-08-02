from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        checksum = 0
        for line in input:
            nums = list(map(int, line.split()))
            checksum += max(nums) - min(nums)

        log.log(log.RESULT, f'The checksum for the spreadsheet is: {checksum}')
        return checksum


part = Part1()

part.add_result(18, """
5 1 9 5
7 5 3
2 4 6 8
""")

part.add_result(32020)
