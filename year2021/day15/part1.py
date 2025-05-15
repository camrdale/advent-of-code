import string

from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate, ParsedMap
from aoc.runner import Part


class RiskMap(ParsedMap):
    def __init__(self, lines: list[str]):
        super().__init__(lines, string.digits)

    def cost(self, from_location: Coordinate, to_location: Coordinate) -> int:
        return int(self.at_location(to_location))


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        map = RiskMap(input)

        _, shortest_path = map.shortest_paths(
            Coordinate(0,0),
            Coordinate(map.max_x, map.max_y))
        assert shortest_path is not None

        log.log(log.RESULT, 'The lowest total risk path is:', shortest_path.length)
        return shortest_path.length


part = Part1()

part.add_result(40, """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""")

part.add_result(393)
