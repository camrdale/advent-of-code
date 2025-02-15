from aoc.log import log, RESULT
from aoc.map import Coordinate
from aoc.runner import Part
from aoc.input import InputParser

from year2023.day17.shared import TrafficMap, Direction


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        map = TrafficMap(parser, 1, 3)

        minimal_heat_loss_path = map.minimal_heat_loss_path(Coordinate(map.min_x,map.min_y), Direction.EAST, Coordinate(map.max_x, map.max_y))

        log(RESULT, f'The least heat loss path is: {minimal_heat_loss_path}')
        return minimal_heat_loss_path


part = Part1()

part.add_result(102, r"""
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
""")

part.add_result(635)
