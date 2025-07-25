from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.assembunny import Computer


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        computer = Computer(input)

        state = computer.run(c=1)

        log.log(log.RESULT, f'Registers contain: {state.registers}')
        return state.registers['a']


part = Part2()

part.add_result(9227771)
