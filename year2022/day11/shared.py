from collections.abc import Callable
import re
from typing import Self


MONKEY_NUM = re.compile(r'Monkey ([0-9]*):')
STARTING_ITEMS = re.compile(r'  Starting items: ([0-9, ]*)')
OPERATION = re.compile(r'  Operation: new = (.*)')
TEST = re.compile(r'  Test: divisible by ([0-9]*)')
IF_TRUE = re.compile(r'    If true: throw to monkey ([0-9]*)')
IF_FALSE = re.compile(r'    If false: throw to monkey ([0-9]*)')

ALL_REGEXES = [MONKEY_NUM, STARTING_ITEMS, OPERATION, TEST, IF_TRUE, IF_FALSE]


class Monkey:
    def __init__(self, num: int, op: Callable[[int], int], test_divisible_by: int, if_true: int, if_false: int):
        self.num = num
        self.operation = op
        self.worry_relief: Callable[[int], int]
        self.test_divisible_by = test_divisible_by
        self.if_true = if_true
        self.if_false = if_false
        self.items: list[int] = []
        self.num_inspections = 0

    @classmethod
    def from_matches(
            cls,
            monkey_matches: dict[re.Pattern[str], tuple[str, ...]]
            ) -> Self:
        num = int(monkey_matches[MONKEY_NUM][0])
        starting_items = map(int, monkey_matches[STARTING_ITEMS][0].split(','))
        op: Callable[[int], int] = eval('lambda old: ' + monkey_matches[OPERATION][0])
        test_divisible_by = int(monkey_matches[TEST][0])
        if_true = int(monkey_matches[IF_TRUE][0])
        if_false = int(monkey_matches[IF_FALSE][0])
        monkey = cls(num, op, test_divisible_by, if_true, if_false)
        for item in starting_items:
            monkey.receive_item(item)
        return monkey
    
    def set_worry_relief(self, worry_relief: Callable[[int], int]):
        self.worry_relief = worry_relief
    
    def receive_item(self, item: int):
        self.items.append(item)

    def inspect_all_items(self, monkeys: dict[int, 'Monkey']):
        while self.items:
            item = self.items.pop(0)
            self.num_inspections += 1
            item = self.operation(item)
            item = self.worry_relief(item)
            if item % self.test_divisible_by == 0:
                monkeys[self.if_true].receive_item(item)
            else:
                monkeys[self.if_false].receive_item(item)

    def print_items(self) -> str:
        return f'Monkey {self.num}: {", ".join(map(str, self.items))}'

    def print_inspections(self) -> str:
        return f'Monkey {self.num} inspected items {self.num_inspections} times'
