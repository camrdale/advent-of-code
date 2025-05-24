from typing import NamedTuple, cast
from collections.abc import Callable
import operator


OPERATIONS: dict[str, Callable[[int, int], int]] = {
    'add': operator.add,
    'mul': operator.mul,
    'div': operator.floordiv,
    'mod': operator.mod,
    'eql': operator.eq
}


class Operation:
    def __init__(self, text: str) -> None:
        self.op, self.register, *remainder = text.split()
        if self.op != 'inp':
            self.operation = OPERATIONS[self.op]
            self.operand: str | int = int(remainder[0]) if remainder[0][0] in '0123456789-' else remainder[0]

    def apply(self, model_number: list[int], registers: dict[str, int]):
        if self.op == 'inp':
            registers[self.register] = model_number.pop(0)
            return
        num = self.operand if type(self.operand) == int else registers[cast(str, self.operand)]
        registers[self.register] = self.operation(registers[self.register], num)


class Monad:
    def __init__(self, input: list[str]) -> None:
        self.operations = [Operation(line) for line in input]

    def validate(self, model_number: list[int]) -> int:
        assert len(model_number) == 14, model_number
        assert max(model_number) <= 9, model_number
        assert min(model_number) >= 1, model_number

        registers = {'w': 0, 'x': 0, 'y': 0, 'z': 0}

        for operation in self.operations:
            operation.apply(model_number, registers)

        assert len(model_number) == 0, model_number
        return registers['z']


class PushedValue(NamedTuple):
    digit: int
    addition: int

    def add(self, num: int) -> 'PushedValue':
        return PushedValue(self.digit, self.addition + num)


class Equality(NamedTuple):
    digit: int
    pushed_value: PushedValue

    def range_for_pushed_digit(self):
        if self.pushed_value.addition <= 0:
            return range(9, abs(self.pushed_value.addition), -1)
        else:
            return range(9 - self.pushed_value.addition, 0, -1)
    
    def digit_value(self, pushed_digit_value: int) -> int:
        return pushed_digit_value + self.pushed_value.addition

    @classmethod
    def parseProgram(cls, input: list[str]) -> list['Equality']:
        equalities: list[Equality] = []
        stack: list[PushedValue] = []

        start = 0
        for digit in range(0, 14):
            sub_program = input[start:start+18]
            match sub_program[4].split()[2]:
                case '1':
                    addition = int(sub_program[15].split()[2])
                    stack.append(PushedValue(digit, addition))
                case '26':
                    pushed_value = stack.pop()
                    addition = int(sub_program[5].split()[2])
                    equalities.append(Equality(digit, pushed_value.add(addition)))
                case _:
                    raise ValueError(f'Failed to parse: {sub_program[4]}')
            start += 18
        
        assert len(stack) == 0, stack

        return equalities
