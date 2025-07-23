from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day23.shared import Computer


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        computer = Computer(input)

        registers = computer.run()

        log.log(log.RESULT, f'Registers contain: {registers}')
        return registers['a']


part = Part1()

part.add_result(3, """
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
""")

part.add_result(10365)
