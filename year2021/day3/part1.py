from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        bits = [[ord(c) - ord('0') for c in line] for line in input]

        # Sum each of the bit positions.
        bit_sums = list(map(sum, zip(*bits)))
        num_bits = len(bits)

        # If the sum is more than half the number of entries, then the most common is 1.
        gamma_bits = [1 if bit_sum > num_bits/2.0 else 0 for bit_sum in bit_sums]
        epsilon_bits = [1 if bit == 0 else 0 for bit in gamma_bits]

        # Convert back to string and parse as a binary number.
        gamma = int("".join(chr(bit + ord('0')) for bit in gamma_bits), 2)
        epsilon = int("".join(chr(bit + ord('0')) for bit in epsilon_bits), 2)

        log(RESULT, 'Power consumption:', gamma*epsilon)
        return gamma*epsilon


part = Part1()

part.add_result(198, """
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

part.add_result(3374136)
