import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


MANUAL = re.compile(r'row ([0-9]*), column ([0-9]*)\.')

START = 20151125
MULTIPLICAND = 252533
DIVISOR = 33554393


def modular_exponent(base: int, exponent: int, modulus: int) -> int:
    result = 1

    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent >>= 1
        base = (base * base) % modulus

    return result


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        manual = MANUAL.search(input[0])
        assert manual is not None

        row = int(manual.group(1))
        column = int(manual.group(2))

        code_num = (row + column - 1) * (row + column) // 2 + 1 - row

        code = START * modular_exponent(MULTIPLICAND, code_num - 1, DIVISOR) % DIVISOR

        log.log(log.RESULT, f'The {code_num}th code is {code}')
        return code


part = Part1()

part.add_result(18749137, """
To continue, please consult the code grid in the manual.  Enter the code at row 1, column 2.
""")

part.add_result(15514188, """
To continue, please consult the code grid in the manual.  Enter the code at row 2, column 5.
""")

part.add_result(1601130, """
To continue, please consult the code grid in the manual.  Enter the code at row 3, column 3.
""")

part.add_result(33071741, """
To continue, please consult the code grid in the manual.  Enter the code at row 6, column 1.
""")

part.add_result(21345942, """
To continue, please consult the code grid in the manual.  Enter the code at row 4, column 3.
""")

part.add_result(19980801)
