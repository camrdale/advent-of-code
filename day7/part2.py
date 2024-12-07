#!/usr/bin/python

from pathlib import Path

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'
TEST_INPUT = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


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
    result = find_equation(
        test_value, 
        current_value * operand, 
        equation + ' * ' + str(operand), 
        remaining_operands[1:])
    if result is not None:
        return result
    return find_equation(
        test_value, 
        int(str(current_value) + str(operand)),
        equation + ' || ' + str(operand), 
        remaining_operands[1:])


input: dict[int, list[int]] = {}
with INPUT_FILE.open() as ifp:
    # for line in TEST_INPUT.split('\n'):
    for line in ifp.readlines():
        text = line.strip()
        if text == '':
            continue
        test_value = int(text.split(':')[0])
        operands = list(map(int, text.split(':')[1].split()))
        input[test_value] = operands

total_calibration_result = 0
for test_value, operands in input.items():
    equation = find_equation(test_value, operands[0], str(operands[0]), operands[1:])
    if equation is None:
        print(test_value, 'is not possible')
    else:
        print(test_value, '=', equation)
        total_calibration_result += test_value

print('Total calibration result:', total_calibration_result)
