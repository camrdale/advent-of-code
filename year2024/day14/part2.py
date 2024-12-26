from aoc.input import InputParser
from aoc.log import log, RESULT, INFO, DEBUG, get_log_level
from aoc.runner import Part

from .shared import RobotMap, ROBOT


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_parsed_input(ROBOT)
        width: int
        height: int
        width, height = parser.get_additional_params()
        robots = RobotMap(input, width, height)

        found: list[tuple[tuple[int, int, int, int], int, str]] = []
        for elapsed in range(10000):
            robots.simulate(1)
            found.append((robots.line_lengths(), elapsed + 1, str(robots)))
        
        if get_log_level() >= INFO:
            for line_lengths, elapsed, robots in sorted(found, reverse=True)[:10]:
                log(INFO, f'Robots after {elapsed} seconds have longest line lengths {line_lengths}')
                log(DEBUG, robots)
        
        top_result = sorted(found, reverse=True)[0]
        log(RESULT, f'Robots after {top_result[1]} seconds have longest line lengths {top_result[0]}')
        log(INFO, top_result[2])
        return top_result[1]

part = Part2()

part.add_result(7572, None, 101, 103)
