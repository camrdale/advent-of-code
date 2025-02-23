from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2019.day23.shared import NicRouter


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))

        router = NicRouter(intcode_input, 50)
        router.start()
        address_255 = router.get_queue(255)
        x = address_255.get_blocking()
        y = address_255.get_blocking()

        log.log(log.RESULT, f'The first packet sent to address 255: x={x},y={y}')
        return y


part = Part1()

part.add_result(20665)
