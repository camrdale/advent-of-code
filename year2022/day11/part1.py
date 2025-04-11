from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day11.shared import Monkey, ALL_REGEXES


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_multipart_parsed_input(*ALL_REGEXES)

        monkeys: dict[int, Monkey] = {}
        for monkey_matches in input:
            monkey = Monkey.from_matches(monkey_matches)
            monkey.set_worry_relief(lambda item: item // 3)
            monkeys[monkey.num] = monkey

        for i in range(20):
            for monkey in monkeys.values():
                monkey.inspect_all_items(monkeys)
            if i == 0 or i == 1 or (i+1) % 5 == 0:
                log.log(log.INFO, f'\nAfter round {i+1}, the monkeys are holding items with these worry levels:')
                for monkey in monkeys.values():
                    log.log(log.INFO, monkey.print_items())
        
        active_monkeys = sorted(monkeys.values(), key=lambda monkey: monkey.num_inspections, reverse=True)
        monkey_business = active_monkeys[0].num_inspections * active_monkeys[1].num_inspections

        log.log(log.RESULT, f'The level of monkey business after 20 rounds: {monkey_business}')
        return monkey_business


part = Part1()

part.add_result(10605, r"""
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""")

part.add_result(112815)
