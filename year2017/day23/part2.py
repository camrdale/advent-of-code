from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day23.shared import Computer, SET, JNZ, SUB, MUL, Operation, State


class MOD(Operation):
    def __init__(self, register: str, value: str) -> None:
        super().__init__()
        self.register = register
        self.value = value

    def apply(self, state: State) -> None:
        state.registers[self.register] %= self.get_value(self.value, state.registers)
        state.instruction += 1
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.register}, {self.value})'


class JLZ(Operation):
    def __init__(self, value: str, register_or_offset: str) -> None:
        super().__init__()
        self.value = value
        self.register_or_offset = register_or_offset

    def apply(self, state: State) -> None:
        if self.get_value(self.value, state.registers) < 0:
            state.instruction += self.get_value(self.register_or_offset, state.registers)
        else:
            state.instruction += 1
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.value}, {self.register_or_offset})'


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        coprocessor = Computer(input)
        coprocessor.state.registers['a'] = 1

        # Original instructions are equivalent to:
        #     for b in range(108400, 125400 + 1, 17):
        #         if not is_prime(b):
        #             h += 1
        # Replace with trial division using modulus

        # First check if b % 2 == 0
        coprocessor.state.instructions[9] = SET('g', 'b')
        coprocessor.state.instructions[10] = MOD('g', '2')
        coprocessor.state.instructions[11] = JNZ('g', '3')
        coprocessor.state.instructions[12] = SET('f', '0')
        coprocessor.state.instructions[13] = JNZ('1', '12')

        # d = 3
        coprocessor.state.instructions[14] = SET('d', '3')
        # Check if b % d == 0
        coprocessor.state.instructions[15] = SET('g', 'b')
        coprocessor.state.instructions[16] = MOD('g', 'd')
        coprocessor.state.instructions[17] = JNZ('g', '3')
        coprocessor.state.instructions[18] = SET('f', '0')
        coprocessor.state.instructions[19] = JNZ('1', '6')
        # d += 2
        coprocessor.state.instructions[20] = SUB('d', '-2')
        # loop while d * d <= b
        #   21: set g d
        coprocessor.state.instructions.insert(22, MUL('g', 'd'))
        #   23: sub g b
        coprocessor.state.instructions[24] = JLZ('g', '-9')

        # Fix final jump offset
        coprocessor.state.instructions[-1] = JNZ('1', '-24')

        log.log(log.INFO, 'Optimized list of instructions:')
        for instruction in coprocessor.state.instructions:
            log.log(log.INFO, instruction)

        coprocessor.run(debug=False)

        log.log(log.RESULT, f'The value in register h: {coprocessor.state.registers['h']}')
        return coprocessor.state.registers['h']


part = Part2()

part.add_result(903)
