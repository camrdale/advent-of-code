from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part
import string


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        sum_calibration_values = 0
        for line in input:
            digits = [c for c in line if c in string.digits]
            s = digits[0]
            digits = [c for c in reversed(line) if c in string.digits]
            s += digits[0]
            calibration_value = int(s)
            log(INFO, f'Got {calibration_value} from: {line}')
            sum_calibration_values += calibration_value

        log(RESULT, f'The sum of all calibration values: {sum_calibration_values}')
        return sum_calibration_values


part = Part1()

part.add_result(142, """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
""")

part.add_result(54601)
