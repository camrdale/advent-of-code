import numpy
import numpy.typing


GRID_SIZE = 300


class PowerGrid:
    def __init__(self, serial_number: int) -> None:
        self.serial_number = serial_number

        row = numpy.arange(1, GRID_SIZE + 1, dtype=numpy.int32)
        x_coords = numpy.tile(row, (GRID_SIZE, 1))
        y_coords = numpy.transpose(x_coords)
        rack_id = x_coords + 10
        power_level = rack_id * y_coords
        power_level += self.serial_number
        power_level *= rack_id
        power_level //= 100
        power_level %= 10
        power_level -= 5

        # Cached dict of sizes, and sum of power cells for squares of that size.
        self.power_squares: dict[int, numpy.typing.NDArray[numpy.int32]] = {
            1: power_level}
    
    def power_square(self, size: int) -> numpy.typing.NDArray[numpy.int32]:
        if size in self.power_squares:
            return self.power_squares[size]
        
        original = self.power_squares[1]
        # Start with the top left of the previous smaller square, and the
        # bottom right corner of the original cell power to add
        result = self.power_square(size-1)[:-1,:-1] + original[size-1:,size-1:]
        for i in range(1, size):
            # Add the next row and column from the original cell power
            result += original[size-1:,i-1:i-size]
            result += original[i-1:i-size,size-1:]
        self.power_squares[size] = result
        return result

    def indices_of_max(self, size: int) -> tuple[int, int]:
        max_index = numpy.argmax(self.power_square(size))
        max_indices = numpy.unravel_index(max_index, (GRID_SIZE-size+1, GRID_SIZE-size+1))
        return int(max_indices[1]) + 1, int(max_indices[0]) + 1
