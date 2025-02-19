import math
import queue

from aoc import log
from aoc.map import Coordinate, LEFT, RIGHT

from year2019 import intcode


class DroneProgram:
    def __init__(self, intcode_input: list[int]):
        self.intcode_input = list(intcode_input)
        self.starting_x_slope: float = -1.0
        self.starting_x_slope_at_y: int = -1
        self.ending_x_slope: float = -1.0
        self.ending_x_slope_at_y: int = -1

    def is_moving(self, location: Coordinate) -> int:
        drone = intcode.Program('DRONE', self.intcode_input)
        drone_input: queue.Queue[int] = queue.Queue()
        drone_output: queue.Queue[int] = queue.Queue()
        drone.execute(drone_input, drone_output)
        drone_input.put(location.x)
        drone_input.put(location.y)
        drone.join()
        result = drone_output.get()
        return result

    def _find_beam(self) -> Coordinate:
        y = 100
        for num_x in range(1, 50):
            spacing = y // (num_x + 1)
            for i in range(0, num_x):
                x = (i+1) * spacing
                location = Coordinate(x, y)
                if self.is_moving(location):
                    return location
        raise ValueError(f'Failed to find the beam')
    
    def _update_starting_slope(self, starting_location: Coordinate) -> None:
        if self.starting_x_slope_at_y < starting_location.y:
            self.starting_x_slope_at_y = starting_location.y
            self.starting_x_slope = starting_location.x / starting_location.y

    def _update_ending_slope(self, ending_location: Coordinate) -> None:
        if self.ending_x_slope_at_y < ending_location.y:
            self.ending_x_slope_at_y = ending_location.y
            self.ending_x_slope = ending_location.x / ending_location.y

    def _initialize_slopes(self) -> None:
        if self.starting_x_slope_at_y >= 0 and self.ending_x_slope_at_y >= 0:
            return
        beam_location = self._find_beam()

        starting_location = beam_location
        while self.is_moving(starting_location):
            starting_location = starting_location.add(LEFT)
            if starting_location.x < 0:
                raise ValueError(f'Failed to find the beam start near {starting_location}')
        starting_location = starting_location.add(RIGHT)
        self._update_starting_slope(starting_location)

        ending_location = beam_location
        while self.is_moving(ending_location):
            ending_location = ending_location.add(RIGHT)
            if ending_location.x > beam_location.y*10:
                raise ValueError(f'Failed to find the beam start near {ending_location}')
        ending_location = ending_location.add(LEFT)
        self._update_ending_slope(ending_location)
    
    def get_beam_start(self, y: int) -> Coordinate:
        self._initialize_slopes()
        initial_x = math.floor(y * self.starting_x_slope)
        location = Coordinate(initial_x, y)
        while self.is_moving(location):
            location = location.add(LEFT)
            if location.x < 0:
                raise ValueError(f'Failed to find the beam start near {initial_x},{y}')
        while not self.is_moving(location):
            location = location.add(RIGHT)
            if location.x > initial_x*10:
                raise ValueError(f'Failed to find the beam start near {initial_x},{y}')
        self._update_starting_slope(location)
        return location
    
    def get_beam_end(self, y: int) -> Coordinate:
        self._initialize_slopes()
        initial_x = math.floor(y * self.ending_x_slope)
        location = Coordinate(initial_x, y)
        while self.is_moving(location):
            location = location.add(RIGHT)
            if location.x > initial_x*10:
                raise ValueError(f'Failed to find the beam end near {initial_x},{y}')
        while not self.is_moving(location):
            location = location.add(LEFT)
            if location.x < 0:
                raise ValueError(f'Failed to find the beam end near {initial_x},{y}')
        self._update_ending_slope(location)
        return location

    def get_beam(self, y: int) -> tuple[Coordinate, Coordinate]:
        return self.get_beam_start(y), self.get_beam_end(y)
    
    def fits_square_of_width(self, top_y: int) -> tuple[int, Coordinate]:
        top_ending_location = self.get_beam_end(top_y)
        bottom_y = top_y + 99
        bottom_starting_location = self.get_beam_start(bottom_y)
        size_y = bottom_starting_location.y - top_ending_location.y + 1
        size_x = top_ending_location.x - bottom_starting_location.x + 1
        log.log(log.INFO, f'Can fit a square of size {size_x}x{size_y} starting at {bottom_starting_location.x},{top_ending_location.y}')
        return size_x, Coordinate(bottom_starting_location.x, top_ending_location.y)
