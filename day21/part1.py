from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part

from .shared import DirectionalRobot, NumericalRobot

class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        directional_robot_2 = DirectionalRobot()

        directional_robot_1 = DirectionalRobot(directional_robot_2)

        numerical_robot = NumericalRobot(directional_robot_1)

        total_complexity = 0
        for line in input:
            presses = numerical_robot.complete_button_presses(line)
            complexity = presses * int(line[:-1])
            log(INFO, f'{line}: has complexity {presses} * {int(line[:-1])} = {complexity}')
            total_complexity += complexity

        log(RESULT, f'Sum of the complexities: {total_complexity}')
        return total_complexity


part = Part1()

part.add_result(126384, """
029A
980A
179A
456A
379A
""")

part.add_result(212488)
