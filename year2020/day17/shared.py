import numpy
import scipy.ndimage


NUM_ITER = 6


class PocketDimension:
    def __init__(self, lines: list[str], dimensions: int) -> None:
        self.dims = dimensions
        layout_input = numpy.array([list(line) for line in lines])
        self.occupied = numpy.zeros(layout_input.shape, dtype=numpy.bool)
        self.occupied[layout_input == '#'] = True
        for new_dim in range(2, self.dims):
            self.occupied = numpy.expand_dims(self.occupied, axis=new_dim)
        self.occupied = numpy.pad(self.occupied, (NUM_ITER, NUM_ITER), constant_values=False)

    def iterate_once(self) -> None:
        new_occupied = self.occupied.copy()

        weights = numpy.ones([3]*self.dims)
        weights[tuple([1]*self.dims)] = 0
        adjacent = scipy.ndimage.convolve(
            self.occupied, weights, output=numpy.uint32, mode='constant', cval=0)

        new_occupied[self.occupied & ~((adjacent == 3) | (adjacent == 2))] = False
        new_occupied[~self.occupied & (adjacent == 3)] = True

        self.occupied = new_occupied

    def print(self) -> str:
        assert self.dims == 3, 'Can only print 3 dimensions'
        lines: list[str] = []
        for z in range(self.occupied.shape[-1]):
            lines.append(f'z = {z}')
            output = numpy.empty(self.occupied.shape[:-1], dtype=numpy.str_)
            output[self.occupied[:,:,z]] = '#'
            output[~self.occupied[:,:,z]] = '.'
            lines.append('\n'.join(numpy.apply_along_axis(lambda row: ''.join(row), 1, output)) + '\n')
        return '\n'.join(lines) + '\n'

    def num_occupied(self) -> int:
        return self.occupied.sum()
