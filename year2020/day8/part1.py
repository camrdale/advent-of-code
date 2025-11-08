from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day8.shared import Computer


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        computer = Computer(input)

        _, registers = computer.run()

        log.log(log.RESULT, f'The accumulator value when instruction repeats: {registers['accumulator']}')
        return registers['accumulator']


part = Part1()

part.add_result(5, """
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

part.add_result(1753)
