from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.map import Coordinate, RIGHT
from aoc.runner import Part

from year2023.day16.shared import BeamMap, Beam


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        map = BeamMap(parser)

        energized_locations = map.energize(Beam(Coordinate(-1,0), RIGHT))
        log(INFO, map.print_map(additional_features={'#': energized_locations}))

        log(RESULT, f'The number of energized tiles: {len(energized_locations)}')
        return len(energized_locations)


part = Part1()

part.add_result(46, r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
""")

part.add_result(7496)
