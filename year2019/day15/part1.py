import aoc.input
from aoc import log
from aoc import runner

from year2019.day15 import shared


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))

        area_map = shared.AreaMap(intcode_input)
        oxygen_location = area_map.explore()

        _, shortest_path = area_map.shortest_paths(
            area_map.starting_point, oxygen_location, shared.WALL)
        if shortest_path is None:
            raise ValueError(f'Failed to find shortest path to Oxygen')
        log.log(log.INFO, area_map.print_map(additional_features={'*': shortest_path.previous}))

        log.log(log.RESULT, f'The fewest number of commands to the Oxygen: {shortest_path.length}')
        return shortest_path.length


part = Part1()

part.add_result(294)
