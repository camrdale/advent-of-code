import string

from aoc.input import InputParser
from aoc import log
from aoc.map import ParsedMap, Coordinate, Offset
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        tree_map = ParsedMap(input, string.digits)

        # Sets of all coordinates that have height >= key value.
        heights: dict[int, set[Coordinate]] = {}
        heights[9] = tree_map.features['9']
        for height in range(8, 0, -1):
            heights[height] = heights[height+1].union(tree_map.features[str(height)])

        edges = [
            (Coordinate(0,0), Offset(1,0), Offset(0,1)),
            (Coordinate(0,0), Offset(0,1), Offset(1,0)),
            (Coordinate(tree_map.max_x,tree_map.max_y), Offset(-1,0), Offset(0,-1)),
            (Coordinate(tree_map.max_x,tree_map.max_y), Offset(0,-1), Offset(-1,0)),
            ]
        
        visible_locations: set[Coordinate] = set()
        for starting_location, edge_direction, look_direction in edges:
            edge_location = starting_location
            while tree_map.valid(edge_location):
                # Trees on the edge are always visible.
                visible_locations.add(edge_location)
                current_height = int(tree_map.at_location(edge_location))
                current_location = edge_location.add(look_direction)

                while tree_map.valid(current_location):
                    if current_height == 9:
                        break
                    if current_location in heights[current_height+1]:
                        visible_locations.add(current_location)
                        current_height = int(tree_map.at_location(current_location))
                    current_location = current_location.add(look_direction)

                edge_location = edge_location.add(edge_direction)

        log.log(log.RESULT, f'The number of visible trees are: {len(visible_locations)}')
        return len(visible_locations)


part = Part1()

part.add_result(21, r"""
30373
25512
65332
33549
35390
""")

part.add_result(1543)
