from abc import ABC, abstractmethod
from collections.abc import Callable
import operator
import re

NUMBER_MONKEY = re.compile(r'([a-z]*): ([0-9-]+)')
OPERATION_MONKEY = re.compile(r'([a-z]*): ([a-z]*) ([\+\-\*\/]) ([a-z]*)')

OPERATORS = {
    '+': operator.add, 
    '-': operator.sub, 
    '*': operator.mul, 
    '/': operator.floordiv}


class Monkey(ABC):
    @abstractmethod
    def yell(self) -> int:
        pass

    def find_humn(self) -> int:
        return 0

    @abstractmethod
    def needs_to_yell(self, value: int):
        pass


class NumberMonkey(Monkey):
    def __init__(self, number: int):
        self.number = number
        
    def yell(self) -> int:
        return self.number

    def needs_to_yell(self, value: int):
        raise ValueError(f'NumberMonkey can only yell {self.number}')


class OperationMonkey(Monkey):
    def __init__(self, operator: Callable[[int, int], int]):
        self.operator = operator
        self._find_humn: int | None = None
        self.lhs: Monkey
        self.rhs: Monkey
    
    def set_operands(self, lhs: 'Monkey', rhs: 'Monkey'):
        self.lhs = lhs
        self.rhs = rhs

    def yell(self) -> int:
        return self.operator(self.lhs.yell(), self.rhs.yell())
    
    def needs_to_yell(self, value: int):
        if self.operator == operator.add:
            if self.find_humn() == -1:
                self.lhs.needs_to_yell(value - self.rhs.yell())
            elif self.find_humn() == 1:
                self.rhs.needs_to_yell(value - self.lhs.yell())
            else:
                raise ValueError(f'Human is not to be found')
        elif self.operator == operator.sub:
            if self.find_humn() == -1:
                self.lhs.needs_to_yell(value + self.rhs.yell())
            elif self.find_humn() == 1:
                self.rhs.needs_to_yell(self.lhs.yell() - value)
            else:
                raise ValueError(f'Human is not to be found')
        elif self.operator == operator.mul:
            if self.find_humn() == -1:
                self.lhs.needs_to_yell(value // self.rhs.yell())
            elif self.find_humn() == 1:
                self.rhs.needs_to_yell(value // self.lhs.yell())
            else:
                raise ValueError(f'Human is not to be found')
        elif self.operator == operator.floordiv:
            if self.find_humn() == -1:
                self.lhs.needs_to_yell(value * self.rhs.yell())
            elif self.find_humn() == 1:
                self.rhs.needs_to_yell(self.lhs.yell() // value)
            else:
                raise ValueError(f'Human is not to be found')
        else:
            raise ValueError(f'Unexpected operator: {self.operator}')

    def find_humn(self) -> int:
        if self._find_humn is not None:
            return self._find_humn
        if type(self.lhs) is Human:
            self._find_humn = -1
        elif type(self.rhs) is Human:
            self._find_humn = 1
        elif self.lhs.find_humn() != 0:
            self._find_humn = -1
        elif self.rhs.find_humn() != 0:
            self._find_humn = 1
        else:
            self._find_humn = 0
        return self._find_humn


class Human(Monkey):
    def __init__(self):
        self._yell: int | None = None

    def yell(self) -> int:
        if self._yell is None:
            raise ValueError(f'Human can not yell yet')
        else:
            return self._yell

    def needs_to_yell(self, value: int):
        self._yell = value

    def find_humn(self) -> int:
        raise ValueError(f'Human IS humn')
