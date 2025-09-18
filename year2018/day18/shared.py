import numpy
import scipy.ndimage

from aoc import log


class WoodedArea:
    def __init__(self, lines: list[str]) -> None:
        area_input = numpy.array([list(line) for line in lines])
        self.area = numpy.zeros(area_input.shape, dtype=numpy.uint32)
        self.area[area_input == '.'] = 1
        self.area[area_input == '|'] = 10
        self.area[area_input == '#'] = 100

    def iterate_once(self) -> None:
        new_area = self.area.copy()

        adjacent = scipy.ndimage.convolve(
            self.area, [[1,1,1],[1,0,1],[1,1,1]], mode='constant', cval=0)
        new_area[(self.area == 1) & (((adjacent // 10) % 10) >= 3)] = 10
        new_area[(self.area == 10) & ((adjacent // 100) >= 3)] = 100
        new_area[(self.area == 100) & ~(((adjacent // 100) >= 1) & (((adjacent // 10) % 10) >= 1))] = 1

        self.area = new_area

    def iterate(self, num_times: int) -> None:
        iterations = 0
        areas = {self.hash(): 0}
        for _ in range(num_times):
            self.iterate_once()
            iterations += 1
            hash = self.hash()
            if hash in areas:
                break
            areas[hash] = iterations
        
        if iterations < num_times:
            last_iteration = areas[self.hash()]
            loop_iterations = iterations - last_iteration
            log.log(log.INFO, f'Found a loop from iteration {last_iteration} to {iterations} of length: {loop_iterations}')
            iterations += ((num_times - iterations) // loop_iterations) * loop_iterations
            while iterations < num_times:
                self.iterate_once()
                iterations += 1

    def hash(self) -> int:
        return hash(self.area.tobytes())

    def print(self) -> str:
        output = numpy.empty(self.area.shape, dtype=numpy.str_)
        output[self.area==1] = '.'
        output[self.area==10] = '|'
        output[self.area==100] = '#'
        return '\n'.join(numpy.apply_along_axis(lambda row: ''.join(row), 1, output)) + '\n'

    def resource_value(self) -> int:
        return (self.area == 10).sum() * (self.area == 100).sum()
