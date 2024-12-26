from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part

from .shared import TopographicMap


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        map = TopographicMap(input)

        trailhead_ratings = 0
        for trailhead in map.trailheads():
            rating = map.rating(trailhead)
            log(INFO, 'Trailhead', trailhead, 'has a rating of', rating)
            trailhead_ratings += rating

        log(RESULT, 'Total trailhead rating:', trailhead_ratings)
        return trailhead_ratings


part = Part2()

part.add_result(227, """
012345
123456
234567
345678
416789
567891
""")

part.add_result(81, """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""")

part.add_result(1372)
