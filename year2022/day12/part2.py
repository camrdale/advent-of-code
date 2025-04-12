from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day12.shared import ReverseHeightMap


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        height_map = ReverseHeightMap(input)

        visited, _ = height_map.shortest_paths(
            height_map.ending_position, height_map.starting_position)
        
        shortest_trail = min(
            visited[starting_location]
            for starting_location in height_map.features['a']
            if starting_location in visited)
        
        log.log(log.RESULT, f'The fewest steps required to move starting from any square with elevation a to the location that should get the best signal: {shortest_trail}')
        return shortest_trail


part = Part2()

part.add_result(29, r"""
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""")

part.add_result(414)
