import aoc.input
from aoc import log
from aoc import runner


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()

        image = list(map(int, input[0]))
        layers = [image[i:(i+150)] for i in range(0, len(image), 150)]
        log.log(log.DEBUG, f'Loaded image with {len(layers)} layers of 25x6 pixels.')

        fewest_zeroes = 151
        fewest_zeroes_layer: list[int] | None = None
        fewest_zeroes_layer_num = -1
        for i, layer in enumerate(layers):
            num_zeroes = sum(pixel == 0 for pixel in layer)
            if num_zeroes < fewest_zeroes:
                fewest_zeroes = num_zeroes
                fewest_zeroes_layer = layer
                fewest_zeroes_layer_num = i

        if fewest_zeroes_layer is None:
            raise ValueError(f'Failed to find a layer with fewer than 151 zeroes')
        log.log(log.INFO, f'Layer {fewest_zeroes_layer_num} has fewest zeroes: {fewest_zeroes}')

        checksum = sum(pixel == 1 for pixel in fewest_zeroes_layer) * sum(pixel == 2 for pixel in fewest_zeroes_layer)
        log.log(log.RESULT, f'Fewest zeroes layer has checksum: {checksum}')
        return checksum


part = Part1()

part.add_result(2440)
