from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day12.shared import Computer


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        computer = Computer(input)

        registers = computer.run()

        log.log(log.RESULT, f'Registers contain: {registers}')
        return registers['a']


part = Part1()

part.add_result(42, """
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
""")

part.add_result(318117)
