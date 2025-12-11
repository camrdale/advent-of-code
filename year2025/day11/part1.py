from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2025.day11.shared import Device


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        devices = Device.from_input(input)
        
        paths_to_out = devices['you'].paths_to_out()

        log.log(log.RESULT, f'The number of paths from "you" to "out": {paths_to_out}')
        return paths_to_out


part = Part1()

part.add_result(5, """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
""")

part.add_result(413)
