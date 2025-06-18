import numpy
import numpy.typing
import scipy.ndimage


def next_state(neighborhood: numpy.typing.NDArray[numpy.float64]) -> int:
    # neighborhood is 3x3 grid around the middle light, flattened to 1-D array
    if neighborhood[4]:
        # sum includes the middle 'on' light, so subtract it
        return 2 <= neighborhood.sum() - 1 <= 3
    return neighborhood.sum() == 3


class LightGrid:
    def __init__(self, input: list[str]) -> None:
        self.width = len(input[0])
        self.height = len(input)
        self.lights = numpy.zeros((self.width, self.height))
        for y, line in enumerate(input):
            for x, c in enumerate(line):
                if c == '#':
                    self.lights[x,y] = 1

    def step(self) -> None:
        self.lights = scipy.ndimage.generic_filter(
            self.lights, function=next_state, size=3, mode='constant')
    
    def num_on(self) -> int:
        return int(self.lights.sum())
    
    def turn_on_corners(self) -> None:
        self.lights[0, 0] = 1
        self.lights[0, self.height - 1] = 1
        self.lights[self.width - 1, self.height - 1] = 1
        self.lights[self.width - 1, 0] = 1
