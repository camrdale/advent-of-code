import collections

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day8.shared import Instruction


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        registers: dict[str, int] = collections.defaultdict(int)
        max_register = 0
        for line in input:
            instruction = Instruction.from_text(line)
            result = instruction.apply(registers)
            if result is not None and result > max_register:
                max_register = result

        log.log(log.RESULT, f'The largest register value ever held is: {max_register}')
        return max_register


part = Part2()

part.add_result(10, """
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
""")

part.add_result(5443)
