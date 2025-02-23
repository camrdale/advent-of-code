from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2019.day23.shared import NicRouter, NAT


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))

        router = NicRouter(intcode_input, 50)
        router.start()
        nat = NAT(router)
        nat.start()
        nat.join()
        if not nat.last_packet_sent:
            raise ValueError(f'NAT never sent a packet')

        log.log(log.RESULT, f'The last packet sent by the NAT to address 0: {nat.last_packet_sent}')
        return nat.last_packet_sent[1]


part = Part2()

part.add_result(13358)
