from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day11.shared import PowerGrid


class Part1(Part):
    def run(self, parser: InputParser) -> str:
        serial_number = int(parser.get_input()[0])

        power_grid = PowerGrid(serial_number)

        max_indices = power_grid.indices_of_max(3)

        log.log(log.RESULT, f'The largest 3x3 fuel cell is at {max_indices} with power: {power_grid.power_square(3).max()}')
        return ','.join(map(str, max_indices))


part = Part1()

part.add_result('33,45', '18')

part.add_result('21,61', '42')

part.add_result('235,63', '5034')
