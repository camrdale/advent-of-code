import functools
from typing import Any

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day13.shared import compare_lists


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_multipart_input()

        all_packets: list[list[Any]] = []
        for lines in input:
            left: list[Any] = eval(lines[0])
            right: list[Any] = eval(lines[1])
            all_packets.append(left)
            all_packets.append(right)
        all_packets.append([[2]])
        all_packets.append([[6]])

        all_packets.sort(key=functools.cmp_to_key(compare_lists))

        decoder_key = 1
        for i, packet in enumerate(all_packets):
            if compare_lists(packet, [[2]]) == 0 or compare_lists(packet, [[6]]) == 0:
                decoder_key *= i+1
        
        log.log(log.RESULT, f'The decoder key for the the distress signals: {decoder_key}')
        return decoder_key


part = Part1()

part.add_result(140, r"""
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""")

part.add_result(20592)
