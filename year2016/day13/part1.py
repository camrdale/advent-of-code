from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate
from aoc.runner import Part

from year2016.day13.shared import OfficeMaze


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        designers_number = int(parser.get_input()[0])
        destination = Coordinate(*parser.get_additional_params()[0])

        maze = OfficeMaze(designers_number)

        _, shortest_path = maze.shortest_paths(Coordinate(1,1), destination)
        assert shortest_path is not None

        log.log(log.INFO, maze.print_map(additional_features={'O': shortest_path.previous}))

        log.log(log.RESULT, f'The fewest steps to reach {destination}: {shortest_path.length}')
        return shortest_path.length


part = Part1()

part.add_result(11, '10', (7, 4))

part.add_result(82, '1362', (31, 39))
