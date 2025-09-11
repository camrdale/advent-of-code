from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day11.shared import PowerGrid, GRID_SIZE


class Part2(Part):
    def run(self, parser: InputParser) -> str:
        serial_number = int(parser.get_input()[0])

        power_grid = PowerGrid(serial_number)

        max_power = power_grid.power_square(1).max()
        max_size = 1
        for size in range(2, GRID_SIZE + 1):
            power_squares = power_grid.power_square(size)
            power = power_squares.max()
            if power > max_power:
                max_power = power
                max_size = size
                log.log(log.INFO, f'The new largest fuel cell square is size {max_size} at {power_grid.indices_of_max(max_size)} with power: {max_power}')

        max_indices = power_grid.indices_of_max(max_size)

        log.log(log.RESULT, f'The largest fuel cell square is size {max_size} at {max_indices} with power: {max_power}')
        return ','.join(map(str, max_indices)) + ',' + str(max_size)


part = Part2()

part.add_result('90,269,16', '18')

part.add_result('232,251,12', '42')

part.add_result('229,251,16', '5034')
