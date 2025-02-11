import queue

import aoc.input
from aoc import log
import aoc.map
from aoc import runner

from year2019 import intcode
from year2019.day11 import shared


class Part2(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> str:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))

        program = intcode.Program('INTCODE', list(intcode_input))
        
        program_input: queue.Queue[int] = queue.Queue()
        robot_input: queue.Queue[int] = queue.Queue()

        robot = shared.HullPaintingRobot('ROBOT', robot_input, program_input, 1)
        robot.start()

        program.execute(program_input, robot_input)
        program.join()

        robot_input.put(-1)
        robot.join()

        re_zero = aoc.map.Offset(
            min(location.x for location in robot.painted_white) - 1,
            min(location.y for location in robot.painted_white) - 1
            ).negate()

        white_squares = set(location.add(re_zero) for location in robot.painted_white)
        width = max(location.x for location in white_squares) + 2
        height = max(location.y for location in white_squares) + 2
        painted_map = aoc.map.EmptyMap(width, height)
        log.log(log.INFO, painted_map.print_map({u'\u2588': white_squares}))

        log.log(log.RESULT, f'See INFO logs for printed image containing: "GLBEPJZP"')
        return 'GLBEPJZP'


part = Part2()

part.add_result('GLBEPJZP')
