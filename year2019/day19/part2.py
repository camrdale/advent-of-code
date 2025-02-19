import math

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2019.day19 import shared


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))

        drone = shared.DroneProgram(intcode_input)

        y = 100
        start_location, end_location = drone.get_beam(y)
        width = end_location.x - start_location.x + 1
        log.log(log.INFO, f'At line {y}, the beam is width {width}')
        
        min_y = math.ceil(y * 100 / width)
        min_width, _ = drone.fits_square_of_width(min_y)
        while min_width >= 100:
            min_y //= 2
            min_width, _ = drone.fits_square_of_width(min_y)

        max_y = math.ceil(min_y * 100 / width)
        max_width, max_location = drone.fits_square_of_width(max_y)
        while max_width < 100:
            max_y *= 2
            max_width, max_location = drone.fits_square_of_width(max_y)

        # Binary search for the first one that fits
        while min_y + 1 != max_y:
            y = (min_y + max_y) // 2
            width, location = drone.fits_square_of_width(y)
            if width < 100:
                min_y = y
                min_width = width
            else:
                max_y = y
                max_width = width
                max_location = location
        
        # Because the width is not monotonically increasing with y, go back until width is
        # 2 less than target to see if there are any locations better than what we found.
        y = max_y
        width = max_width
        while width > 98:
            y = y - 1
            width, location = drone.fits_square_of_width(y)
            if width == 100:
                max_y = y
                max_width = width
                max_location = location

        log.log(log.RESULT, f'The first line that supports a square of {max_width}x100 is {max_y}, the closest point to the emitter is: {max_location}')
        return max_location.x*10000 + max_location.y


part = Part1()

part.add_result(9231141)
