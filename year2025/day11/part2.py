from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2025.day11.shared import Device


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        devices = Device.from_input(input)
        
        paths_to_out = devices['svr'].paths_to_out_through_fft_and_dac(False, False)

        log.log(log.RESULT, f'The number of paths from "svr" to "out" through "dac" and "fft": {paths_to_out}')
        return paths_to_out


part = Part1()

part.add_result(2, """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
""")

part.add_result(525518050323600)
