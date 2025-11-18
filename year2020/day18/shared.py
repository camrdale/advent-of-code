from collections.abc import Callable
import operator
from typing import Self


OPERATORS: dict[str, Callable[[int, int], int]] = {
    '+': operator.add,
    '*': operator.mul,
}


class Expression:
    def __init__(self, input: str, add_first: bool) -> None:
        values =  [
            int(v)
            for i, v in enumerate(input.split(' '))
            if i % 2 == 0
        ]
        operators =  [
            OPERATORS[v]
            for i, v in enumerate(input.split(' '))
            if i % 2 != 0
        ]

        while operators:
            i = 0
            if add_first and operator.add in operators:
                i = operators.index(operator.add)

            op = operators.pop(i)
            values[i] = op(values[i], values.pop(i + 1))

        self.left = values[0]

    @classmethod
    def parse(cls, input: str, add_first: bool = False) -> tuple[Self, str]:
        while True:
            open_sub = input.find('(')
            close_sub = input.find(')')
            if open_sub == -1 or close_sub < open_sub:
                if close_sub == -1:
                    return cls(input, add_first), ''
                return cls(input[:close_sub], add_first), input[close_sub+1:]
            sub_exp, remaining = Expression.parse(input[open_sub+1:], add_first=add_first)
            input = input[:open_sub] + str(sub_exp.value()) + remaining

    def value(self) -> int:
        return self.left
