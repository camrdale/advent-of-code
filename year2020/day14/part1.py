import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


MASK = re.compile(r'mask = ([X10]*)')
MEM = re.compile(r'mem\[([0-9]*)\] = ([0-9]*)')


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        and_mask = 0
        or_mask = 0
        memory: dict[int, int] = {}
        for line in input:
            mem = MEM.fullmatch(line)

            if mem is None:
                mask = MASK.fullmatch(line)
                assert mask is not None, line
                and_mask = int(mask.group(1).replace('X', '1'), 2)
                or_mask = int(mask.group(1).replace('X', '0'), 2)
                continue

            memory[int(mem.group(1))] = (int(mem.group(2)) & and_mask) | or_mask

        sum_memory = sum(memory.values())
        log.log(log.RESULT, f'The sum of all the {len(memory)} memory values: {sum_memory}')
        return sum_memory


part = Part1()

part.add_result(165, """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
""")

part.add_result(6631883285184)
