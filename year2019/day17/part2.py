import aoc.input
from aoc import log
from aoc import runner

from year2019.day17 import shared


class Part2(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))

        ascii = shared.AsciiProgram(intcode_input)
        result = ascii.find_and_run_path()
   
        log.log(log.RESULT, f'The dust collected by the robot: {result}')
        return result


part = Part2()

part.add_result(942367)
