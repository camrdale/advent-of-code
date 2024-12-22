from aoc.input import InputParser
from aoc.log import log, RESULT, INFO, DEBUG
from aoc.runner import Part

from .shared import RobotMap


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        width: int
        height: int
        width, height = parser.get_additional_params()
        robots = RobotMap(input, width, height)
        
        log(DEBUG, robots)

        robots.simulate(100)

        log(INFO, robots)

        safety_factor = robots.safety_factor()
        log(RESULT, 'Safety factor after 100s:', safety_factor)
        return safety_factor


part = Part1()

part.add_result(12, """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
""", 11, 7)

part.add_result(221616000, None, 101, 103)
