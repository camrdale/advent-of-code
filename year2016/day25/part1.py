from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day25.shared import Computer, JNZ


def is_clock(output: list[int]) -> bool:
    if any(output[i] != 0 for i in range(0, len(output), 2)):
        return False
    if any(output[i] != 1 for i in range(1, len(output), 2)):
        return False
    if output[-1] != 1:
        return False
    return True


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        computer = Computer(input)

        # Make the final instruction not recurse forever.
        computer.instructions[-1] = JNZ('0', '0')

        a = 0
        while True:
            computer.run(a=a)
            log.log(log.INFO, a, computer.output)
            if is_clock(computer.output):
                break
            a += 1

        log.log(log.RESULT, f'For an "a" value of {a}, output is: {computer.output}')
        return a


part = Part1()

part.add_result(196)
