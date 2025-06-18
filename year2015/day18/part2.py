from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2015.day18.shared import LightGrid


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        steps = int(parser.get_additional_params()[0])

        lights = LightGrid(input)
        lights.turn_on_corners()

        for _ in range(steps):
            lights.step()
            lights.turn_on_corners()

        num_on = lights.num_on()

        log.log(log.RESULT, f'After {steps} steps, the number of on lights: {num_on}')
        return num_on


part = Part2()

part.add_result(17, """
.#.#.#
...##.
#....#
..#...
#.#..#
####..
""", 5)

part.add_result(1006, None, 100)
