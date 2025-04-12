from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day12.shared import ReverseHeightMap


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        height_map = ReverseHeightMap(input)

        _, shortest_path = height_map.shortest_paths(
            height_map.ending_position, height_map.starting_position)
        if shortest_path is None:
            raise ValueError(f'Failed to find shortest path')
        
        log.log(log.RESULT, f'The number of steps to the best signal: {shortest_path.length}')
        return shortest_path.length


part = Part1()

part.add_result(31, r"""
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""")

part.add_result(420)
