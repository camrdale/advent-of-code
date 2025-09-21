from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.chronal import Computer, Operation


class DIVI(Operation):
    """(div immediate) stores into register C the result of register A DIV value B."""
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = registers[self.a] // self.b


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        computer = Computer(input)

        # Speed up the execution by replacing lines 19-28 with one operation
        computer.instructions[17] = DIVI(1, 256, 1)
        del computer.instructions[18:27]
        computer.instructions[16].a -= 9
        log.log(log.DEBUG, computer.instructions)

        registers = {i: 0 for i in range(6)}
        found: set[int] = set()
        while True:
            last_registers = registers.copy()
            computer.run(registers, run_until_instruction=19)
            if registers[3] in found:
                break
            found.add(registers[3])
            computer.run(registers, run_until_instruction=20)

        log.log(log.RESULT, f'The registers after a halt with the largest possible number of operations ({computer.num_executed}): {last_registers}')
        return last_registers[3]


part = Part1()

part.add_result(12464363)
