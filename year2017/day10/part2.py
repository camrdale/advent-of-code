import functools
import operator

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day10.shared import knot_hash


class Part1(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()[0]

        lengths = [ord(c) for c in input] + [17, 31, 73, 47, 23]

        l = knot_hash(lengths, repeat=64)

        dense_hash: list[int] = [
            functools.reduce(operator.xor, l[i*16:(i+1)*16])
            for i in range(16)]
        knot_hash_hex = ''.join(format(i, '#04x')[2:] for i in dense_hash)

        log.log(log.RESULT, f'The knot hash is {dense_hash} in hex: {knot_hash_hex}')
        return knot_hash_hex


part = Part1()

part.add_result('a2582a3a0e66e6e86e3812dcb672a272', """

""")

part.add_result('33efeb34ea91902bb2f59c9920caa6cd', """
AoC 2017
""")

part.add_result('3efbe78a8d82f29979031a4aa0b16a9d', """
1,2,3
""")

part.add_result('63960835bcdc130f0b66d7ff4f6a5a8e', """
1,2,4
""")

part.add_result('0c2f794b2eb555f7830766bf8fb65a16')
