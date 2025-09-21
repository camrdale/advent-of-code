from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.chronal import Computer
from year2018.day19.shared import run_optimized


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        computer = Computer(input)

        registers = {i: 0 for i in range(6)}
        run_optimized(computer, registers)

        log.log(log.RESULT, f'The registers after the program finishes: {registers}')
        return registers[0]


part = Part1()

part.add_result(1228)
