import string

from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate, ParsedMap
from aoc.runner import Part


class RiskMap(ParsedMap):
    def __init__(self, lines: list[str]):
        super().__init__(lines, string.digits)
        self.tile_width = self.max_x + 1
        self.tile_height = self.max_y + 1
        self.tiled_max_x = 5 * self.tile_width - 1
        self.tiled_max_y = 5 * self.tile_height - 1

    def cost(self, from_location: Coordinate, to_location: Coordinate) -> int:
        risk = int(self.at_location(Coordinate(
            to_location.x % self.tile_width,
            to_location.y % self.tile_height)))
        x_tile = to_location.x // self.tile_width
        y_tile = to_location.y // self.tile_height
        return (risk - 1 + x_tile + y_tile) % 9 + 1
    
    def valid(self, coordinate: Coordinate) -> bool:
        return self.min_x <= coordinate.x <= self.tiled_max_x and self.min_y <= coordinate.y <= self.tiled_max_y


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        map = RiskMap(input)

        _, shortest_path = map.shortest_paths(
            Coordinate(0,0),
            Coordinate(map.tiled_max_x, map.tiled_max_y))
        assert shortest_path is not None

        log.log(log.RESULT, 'The lowest total risk path is:', shortest_path.length)
        return shortest_path.length


part = Part2()

part.add_result(315, """
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

part.add_result(2823)
