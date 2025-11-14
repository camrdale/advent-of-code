import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


MASK = re.compile(r'mask = ([X10]*)')
MEM = re.compile(r'mem\[([0-9]*)\] = ([0-9]*)')


def generate_addresses(mask: str, mem_address: int) -> list[int]:
    addresses = ['']
    for m, a in zip(mask, f'{mem_address:0{36}b}'):
        b = a if m == '0' else '1' if m == '1' else 'X'
        new_addresses: list[str] = []
        for address in addresses:
            if b == '0' or b == 'X':
                new_addresses.append(address + '0')
            if b == '1' or b == 'X':
                new_addresses.append(address + '1')
        addresses = new_addresses
    return [int(address, 2) for address in addresses]


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        mask = ''
        memory: dict[int, int] = {}
        for line in input:
            mem = MEM.fullmatch(line)

            if mem is None:
                mask_input = MASK.fullmatch(line)
                assert mask_input is not None, line
                mask = mask_input.group(1)
                continue

            memory.update(dict.fromkeys(generate_addresses(mask, int(mem.group(1))), int(mem.group(2))))

        sum_memory = sum(memory.values())
        log.log(log.RESULT, f'The sum of all the {len(memory)} memory values: {sum_memory}')
        return sum_memory


part = Part2()

part.add_result(208, """
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
""")

part.add_result(3161838538691)
