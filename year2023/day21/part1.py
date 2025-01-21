import aoc.input
from aoc import log
from aoc import runner

from year2023.day21 import shared


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()
        num_steps: int
        num_steps, = parser.get_additional_params()

        map = shared.GardenMap(input)
        reachable = map.reachable_plots(map.starting_point, num_steps)
        log.log(log.INFO, map.print_map({'O': reachable}))
        log.log(log.RESULT, f'Reachable plots in {num_steps} steps: {len(reachable)}')
        return len(reachable)


part = Part1()

part.add_result(16, r"""
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
""", 6)

part.add_result(3594, None, 64)
