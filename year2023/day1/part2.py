from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part
import string


NUMBERS: list[str] = list(string.digits) + [
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        sum_calibration_values = 0
        for line in input:
            calibration_string = ''
            for i in range(len(line)):
                for index, value in enumerate(NUMBERS):
                    if line[i:].startswith(value):
                        if len(calibration_string) == 0:
                            calibration_string += str(index % 10)
                        calibration_string = calibration_string[0] + str(index % 10)
                        break

            calibration_value = int(calibration_string)
            log(INFO, f'Got {calibration_value} from: {line}')
            sum_calibration_values += calibration_value

        log(RESULT, f'The sum of all calibration values: {sum_calibration_values}')
        return sum_calibration_values


part = Part2()

part.add_result(281, """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
""")

part.add_result(54078)
