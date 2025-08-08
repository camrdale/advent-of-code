import collections

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day8.shared import Instruction


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        registers: dict[str, int] = collections.defaultdict(int)
        for line in input:
            instruction = Instruction.from_text(line)
            instruction.apply(registers)

        max_register = max(registers.values())
        log.log(log.RESULT, f'The largest register value is: {max_register}')
        return max_register


part = Part1()

part.add_result(1, """
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
""")

part.add_result(4832)
