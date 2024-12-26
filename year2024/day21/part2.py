from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part

from .shared import DirectionalRobot, NumericalRobot


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        directional_robot = DirectionalRobot()

        for _ in range(24):
            directional_robot = DirectionalRobot(directional_robot)

        numerical_robot = NumericalRobot(directional_robot)

        total_complexity = 0
        for line in input:
            num_presses = numerical_robot.complete_button_presses(line)
            complexity = num_presses * int(line[:-1])
            log(INFO, f'{line}: has complexity {num_presses} * {int(line[:-1])} = {complexity}')
            total_complexity += complexity

        log(RESULT, f'Sum of the complexities: {total_complexity}')
        return total_complexity


part = Part2()

part.add_result(258263972600402)
