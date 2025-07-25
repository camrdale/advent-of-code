import math

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.assembunny import Computer, TGL, CPY, JNZ


def shortcut(computer: Computer) -> int:
    for i, instruction in enumerate(computer.instructions):
        if isinstance(instruction, TGL):
            cpy = computer.instructions[i + 3]
            assert isinstance(cpy, CPY)
            cpy_value = int(cpy.value)
            jnz = computer.instructions[i + 4]
            assert isinstance(jnz, JNZ)
            jnz_value = int(jnz.value)
            result = math.factorial(12) + (cpy_value * jnz_value)
            log.log(log.RESULT, f'Expect register "a" to contain: {result}')
            return result
    raise ValueError(f'Failed to find the TGL instruction.')


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        computer = Computer(input)

        # return shortcut(computer)

        # Takes 20 minutes to run without optimizations
        state = computer.run(a=12)

        log.log(log.RESULT, f'Registers contain: {state.registers}')
        return state.registers['a']


part = Part2()

part.add_result(479006925)
