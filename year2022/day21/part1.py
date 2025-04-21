from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day21.shared import Monkey, NumberMonkey, OperationMonkey, NUMBER_MONKEY, OPERATION_MONKEY, OPERATORS


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        monkeys: dict[str, Monkey] = {}
        operation_monkeys: dict[str, tuple[str, str]] = {}
        for line in input:
            if match := NUMBER_MONKEY.match(line):
                monkeys[match.group(1)] = NumberMonkey(int(match.group(2)))
            elif match := OPERATION_MONKEY.match(line):
                monkeys[match.group(1)] = OperationMonkey(OPERATORS[match.group(3)])
                operation_monkeys[match.group(1)] = (match.group(2), match.group(4))
            else:
                raise ValueError(f'Unmatched line: {line}')
        
        for monkey, (lhs, rhs) in operation_monkeys.items():
            operation_monkey = monkeys[monkey]
            assert type(operation_monkey) is OperationMonkey
            operation_monkey.set_operands(monkeys[lhs], monkeys[rhs])

        root_yells = monkeys['root'].yell()
        log.log(log.RESULT, f'The monkey named root will yell: {root_yells}')
        return root_yells


part = Part1()

part.add_result(152, r"""
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
""")

part.add_result(286698846151845)
