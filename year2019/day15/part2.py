import aoc.input
from aoc import log
from aoc import runner

from year2019.day15 import shared


class Part2(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))

        area_map = shared.AreaMap(intcode_input)
        oxygen_location = area_map.explore()

        all_locations, _ = area_map.shortest_paths(
            oxygen_location, area_map.starting_point, shared.WALL)
        time_to_fill = max(all_locations.values())

        log.log(log.RESULT, f'The number of minutes to fill all locations: {time_to_fill}')
        return time_to_fill


part = Part2()

part.add_result(388)
