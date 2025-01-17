from aoc.log import log, RESULT
from aoc.map import Coordinate
from aoc.runner import Part
from aoc.input import InputParser

from year2023.day17.shared import TrafficMap, Direction


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        map = TrafficMap(parser, 4, 10)

        minimal_heat_loss_path = map.minimal_heat_loss_path(Coordinate(0,0), Direction.EAST, Coordinate(map.width - 1, map.height - 1))

        log(RESULT, f'The least heat loss path is: {minimal_heat_loss_path}')
        return minimal_heat_loss_path


part = Part2()

part.add_result(94, r"""
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

part.add_result(71, r"""
111111111111
999999999991
999999999991
999999999991
999999999991
""")

part.add_result(734)
