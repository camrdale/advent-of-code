from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2021.day16.shared import Packet


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        packet = Packet.from_text(input[0])

        versions = packet.sum_versions()
        log.log(log.RESULT, 'The sum of the version numbers of the packets:', versions)
        return versions


part = Part1()

part.add_result(6, """
D2FE28
""")

part.add_result(9, """
38006F45291200
""")

part.add_result(14, """
EE00D40C823060
""")

part.add_result(16, """
8A004A801A8002F478
""")

part.add_result(12, """
620080001611562C8802118E34
""")

part.add_result(23, """
C0015000016115A2E0802F182340
""")

part.add_result(31, """
A0016C880162017C3686B18A3D4780
""")

part.add_result(989)
