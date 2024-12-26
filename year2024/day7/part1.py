from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part


def find_equation(
        test_value: int, 
        current_value: int, 
        equation: str,
        remaining_operands: list[int]
        ) -> str | None:
    """Find an equation that gives the test value."""
    if len(remaining_operands) == 0:
        # All operands have been considered.
        if current_value == test_value:
            return equation
        return None
    if current_value > test_value:
        # Short circuit, return early if the value is not possible.
        return None
    operand = remaining_operands[0]
    result = find_equation(
        test_value, 
        current_value + operand, 
        equation + ' + ' + str(operand), 
        remaining_operands[1:])
    if result is not None:
        return result
    return find_equation(
        test_value, 
        current_value * operand, 
        equation + ' * ' + str(operand), 
        remaining_operands[1:])


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        raw_input = parser.get_input()

        input: dict[int, list[int]] = {}
        for line in raw_input:
            test_value = int(line.split(':')[0])
            operands = list(map(int, line.split(':')[1].split()))
            input[test_value] = operands

        total_calibration_result = 0
        for test_value, operands in input.items():
            equation = find_equation(test_value, operands[0], str(operands[0]), operands[1:])
            if equation is None:
                log(INFO, test_value, 'is not possible')
            else:
                log(INFO, test_value, '=', equation)
                total_calibration_result += test_value

        log(RESULT, 'Total calibration result:', total_calibration_result)
        return total_calibration_result


part = Part1()

part.add_result(3749, """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""")

part.add_result(4998764814652)
