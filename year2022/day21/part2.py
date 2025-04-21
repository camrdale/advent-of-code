from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day21.shared import Monkey, NumberMonkey, OperationMonkey, Human, NUMBER_MONKEY, OPERATION_MONKEY, OPERATORS

class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        monkeys: dict[str, Monkey] = {}
        operation_monkeys: dict[str, tuple[str, str]] = {}
        for line in input:
            if match := NUMBER_MONKEY.match(line):
                if match.group(1) == 'humn':
                    monkeys[match.group(1)] = Human()
                else:
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
       
        root_monkey = monkeys['root']
        assert type(root_monkey) is OperationMonkey
        root_human = root_monkey.find_humn()
        if root_human == -1:
            value = root_monkey.rhs.yell()
            root_monkey.lhs.needs_to_yell(value)
        elif root_human == 1:
            value = root_monkey.lhs.yell()
            root_monkey.rhs.needs_to_yell(value)
        else:
            raise ValueError(f'Failed to find human')
        
        human_yells = monkeys['humn'].yell()

        log.log(log.RESULT, f'The human needs to yell: {human_yells}')
        return human_yells


part = Part2()

part.add_result(301, r"""
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

part.add_result(3759566892641)
