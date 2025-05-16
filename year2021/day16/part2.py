from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2021.day16.shared import Packet


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        packet = Packet.from_text(input[0])

        value = packet.value()
        log.log(log.RESULT, 'The value of the packet:', value)
        return value


part = Part2()

part.add_result(3, """
C200B40A82
""")

part.add_result(54, """
04005AC33890
""")

part.add_result(7, """
880086C3E88112
""")

part.add_result(9, """
CE00C43D881120
""")

part.add_result(1, """
D8005AC2A8F0
""")

part.add_result(0, """
F600BC2D8F
""")

part.add_result(0, """
9C005AC2F8F0
""")

part.add_result(1, """
9C0141080250320F1802104A08
""")

part.add_result(7936430475134)
