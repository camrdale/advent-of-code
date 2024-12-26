from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        bits = [[ord(c) - ord('0') for c in line] for line in input]

        o2_bits = list(bits)
        position = 0
        while len(o2_bits) > 1:
            bit_sums = list(map(sum, zip(*o2_bits)))
            num_bits = len(o2_bits)
            most_common = 1 if bit_sums[position] >= num_bits/2.0 else 0
            o2_bits[:] = [bits for bits in o2_bits if bits[position] == most_common]
            position += 1

        co2_bits = list(bits)
        position = 0
        while len(co2_bits) > 1:
            bit_sums = list(map(sum, zip(*co2_bits)))
            num_bits = len(co2_bits)
            most_common = 1 if bit_sums[position] < num_bits/2.0 else 0
            co2_bits[:] = [bits for bits in co2_bits if bits[position] == most_common]
            position += 1

        # Convert back to string and parse as a binary number.
        o2 = int("".join(chr(bit + ord('0')) for bit in o2_bits[0]), 2)
        co2 = int("".join(chr(bit + ord('0')) for bit in co2_bits[0]), 2)

        log(RESULT, 'Life support rating:', o2 * co2)
        return o2 * co2


part = Part2()

part.add_result(230, """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
""")

part.add_result(4432698)
