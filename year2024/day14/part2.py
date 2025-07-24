import concurrent.futures
import sys

from aoc.input import InputParser
from aoc.log import log, RESULT, INFO, DEBUG, get_log_level, ProgressBar
from aoc.runner import Part

from .shared import RobotMap, ROBOT


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_parsed_int_input(ROBOT)
        width: int
        height: int
        width, height = parser.get_additional_params()

        found: list[tuple[tuple[int, int, int, int], int, str]] = []

        def simulate_robots(elapsed: int) -> tuple[tuple[int, int, int, int], int, str]:
            robots = RobotMap(input, width, height)
            robots.simulate(elapsed + 1)
            return (robots.line_lengths(), elapsed + 1, str(robots))

        assert not sys._is_gil_enabled() # type: ignore
        with ProgressBar(10000, desc='day 14,2') as progress_bar:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures: list[concurrent.futures.Future[tuple[tuple[int, int, int, int], int, str]]] = []
                for elapsed in range(10000):
                    futures.append(executor.submit(simulate_robots, elapsed))
                for future in concurrent.futures.as_completed(futures):
                    progress_bar.update()
                    found.append(future.result())

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
