from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day24.shared import BlizzardMap, Coordinate


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        blizzard_map = BlizzardMap(input)

        shortest_path = blizzard_map.shortest_path(
            Coordinate(blizzard_map.min_x + 1, blizzard_map.min_y),
            Coordinate(blizzard_map.max_x - 1, blizzard_map.max_y))
        shortest_path = blizzard_map.shortest_path(
            Coordinate(blizzard_map.max_x - 1, blizzard_map.max_y),
            Coordinate(blizzard_map.min_x + 1, blizzard_map.min_y))
        shortest_path = blizzard_map.shortest_path(
            Coordinate(blizzard_map.min_x + 1, blizzard_map.min_y),
            Coordinate(blizzard_map.max_x - 1, blizzard_map.max_y))

        log.log(log.RESULT, f'The shortest path back and forth requires minutes: {shortest_path}')
        return shortest_path


part = Part1()

part.add_result(54, r"""
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
""")

part.add_result(908)
