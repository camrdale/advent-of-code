import queue

import aoc.input
from aoc import log
from aoc import runner

from year2019 import intcode
from year2019.day11 import shared


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))

        program = intcode.Program('INTCODE', list(intcode_input))
        
        program_input: queue.Queue[int] = queue.Queue()
        robot_input: queue.Queue[int] = queue.Queue()

        robot = shared.HullPaintingRobot('ROBOT', robot_input, program_input, 0)
        robot.start()

        program.execute(program_input, robot_input)
        program.join()

        robot_input.put(-1)
        robot.join()

        log.log(log.RESULT, f'Hull painting robot painted {len(robot.painted)} panels')
        return len(robot.painted)


part = Part1()

part.add_result(2056)
