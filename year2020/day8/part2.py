from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day8.shared import Computer, JMP, NOP


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        computer = Computer(input)

        for i in range(len(computer.instructions)):
            orig_instruction = computer.instructions[i]
            if isinstance(orig_instruction, JMP):
                computer.instructions[i] = NOP(orig_instruction.offset)
            elif isinstance(orig_instruction, NOP):
                computer.instructions[i] = JMP(orig_instruction.offset)
            else:
                continue
            finished, registers = computer.run()
            if finished:
                log.log(log.INFO, f'Changing instruction {i} from {type(orig_instruction)} caused program to finish')
                log.log(log.RESULT, f'The accumulator value when program finishes: {registers['accumulator']}')
                return registers['accumulator']
            computer.instructions[i] = orig_instruction

        raise ValueError(f'Failed to find an instruction to change that causes the program to finish')


part = Part2()

part.add_result(8, """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
""")

part.add_result(733)
