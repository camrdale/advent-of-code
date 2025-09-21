from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.chronal import Computer


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        computer = Computer(input)

        registers = {i: 0 for i in range(6)}
        computer.run(registers, run_until_instruction=28)

        registers[0] = registers[3]
        computer.run(registers)

        log.log(log.RESULT, f'The registers after a halt with the smalllest possible number of operations ({computer.num_executed}): {registers}')
        return registers[0]


part = Part1()

part.add_result(3173684)
