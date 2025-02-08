import aoc.input
from aoc import log
from aoc import runner


class Part2(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> str:
        input = parser.get_input()

        image = list(map(int, input[0]))

        pixels = [image[i:len(image):150] for i in range(150)]
        log.log(log.DEBUG, f'Loaded image with {len(pixels)} pixels (25x6), each of length {len(pixels[0])}.')

        decoded_pixels = [next(i for i in pixel if i != 2) for pixel in pixels]

        for i in range(len(decoded_pixels) // 25):
            log.log(log.INFO, ''.join(' ' if pixel == 1 else u'\u2588' for pixel in decoded_pixels[i*25:(i+1)*25]))

        log.log(log.RESULT, f'See INFO logs for printed image containing: "AZCJC"')
        return 'AZCJC'


part = Part2()

part.add_result('AZCJC')
