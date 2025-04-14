from aoc.input import InputParser
from aoc.log import log, RESULT, INFO, progress_bar
from aoc.map import Coordinate, UP, RIGHT, DOWN, LEFT
from aoc.runner import Part

from year2023.day16.shared import BeamMap, Beam


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        map = BeamMap(parser)

        max_energized = 0
        max_energized_locations: set[Coordinate] = set()
        for y in progress_bar(range(map.min_y, map.max_y + 1), desc='day 16,2 1/2'):
            energized_locations = map.energize(Beam(Coordinate(-1,y), RIGHT))
            if len(energized_locations) > max_energized:
                max_energized = len(energized_locations)
                max_energized_locations = energized_locations
            energized_locations = map.energize(Beam(Coordinate(map.max_x+1,y), LEFT))
            if len(energized_locations) > max_energized:
                max_energized = len(energized_locations)
                max_energized_locations = energized_locations
        for x in progress_bar(range(map.min_x, map.max_x + 1), desc='day 16,2 2/2'):
            energized_locations = map.energize(Beam(Coordinate(x,-1), DOWN))
            if len(energized_locations) > max_energized:
                max_energized = len(energized_locations)
                max_energized_locations = energized_locations
            energized_locations = map.energize(Beam(Coordinate(x,map.max_y+1), UP))
            if len(energized_locations) > max_energized:
                max_energized = len(energized_locations)
                max_energized_locations = energized_locations

        log(INFO, map.print_map(additional_features={'#': max_energized_locations}))

        log(RESULT, f'The maximum number of energized tiles: {max_energized}')
        return max_energized


part = Part2()

part.add_result(51, r"""
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

part.add_result(7932)
