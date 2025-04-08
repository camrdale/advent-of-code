import string

from aoc.input import InputParser
from aoc import log
from aoc.map import ParsedMap, Coordinate, NEIGHBORS
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        tree_map = ParsedMap(input, string.digits)

        # Sets of all coordinates that have height >= key value.
        heights: dict[int, set[Coordinate]] = {}
        heights[9] = tree_map.features['9']
        for height in range(8, -1, -1):
            heights[height] = heights[height+1].union(tree_map.features[str(height)])

        max_scenic_score = 0
        best_location = Coordinate(-1,-1)
        for x in range(1, tree_map.max_x):
            for y in range(1, tree_map.max_y):
                location = Coordinate(x,y)
                height = int(tree_map.at_location(location))
                scenic_score = 1
                for direction in NEIGHBORS:
                    visible = 0
                    neighbor_location = location.add(direction)
                    while tree_map.valid(neighbor_location):
                        visible += 1
                        if neighbor_location in heights[height]:
                            break
                        neighbor_location = neighbor_location.add(direction)
                    scenic_score = scenic_score * visible

                if scenic_score > max_scenic_score:
                    max_scenic_score = scenic_score
                    best_location = location
                    log.log(log.INFO, f'Found new best scenic score of {max_scenic_score} at: {best_location}')
        
        log.log(log.RESULT, f'The best scenic score is {max_scenic_score} at: {best_location}')
        return max_scenic_score


part = Part2()

part.add_result(8, r"""
30373
25512
65332
33549
35390
""")

part.add_result(595080)
