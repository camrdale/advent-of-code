from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        num_zeros = 0
        dial = 50
        for line in input:
            rotation = int(line[1:])
            for _ in range(rotation):
                dial = (dial + (-1 if line[0] == 'L' else 1)) % 100
                if dial == 0:
                    num_zeros += 1

        log.log(log.RESULT, f'The number of times the dial pointed at zero: {num_zeros}')
        return num_zeros


part = Part2()

part.add_result(6, """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
""")

part.add_result(10, """
R1000
""")

part.add_result(5892)
