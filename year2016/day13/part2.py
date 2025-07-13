from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate
from aoc.runner import Part

from year2016.day13.shared import OfficeMaze


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        designers_number = int(parser.get_input()[0])

        maze = OfficeMaze(designers_number)

        visited, _ = maze.shortest_paths(Coordinate(1,1), Coordinate(1,1))

        log.log(log.INFO, maze.print_map())

        num_locations = len([steps for steps in visited.values() if steps <= 50])
        log.log(log.RESULT, f'The number of locations (of {len(visited)}) that can be readched in 50 steps: {num_locations}')
        return num_locations


part = Part2()

part.add_result(138, '1362')
