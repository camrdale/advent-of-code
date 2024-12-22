from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part

from .shared import TopographicMap


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        map = TopographicMap(input)

        trailhead_scores = 0
        for trailhead in map.trailheads():
            score = map.score(trailhead)
            log(INFO, 'Trailhead', trailhead, 'has a score of', score)
            trailhead_scores += score

        log(RESULT, 'Total trailhead score:', trailhead_scores)
        return trailhead_scores


part = Part1()

part.add_result(1, """
0123
1234
8765
9876
""")

part.add_result(36, """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""")

part.add_result(674)
