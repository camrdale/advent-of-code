from collections.abc import Generator
from typing import NoReturn, Any

import numpy
import numpy.typing

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


GEN_A_FACTOR = 16807
GEN_B_FACTOR = 48271
DIVISOR = 2147483647
BIT_MASK = 0xFFFF
NUM_PAIRS = 5_000_000


# 5 seconds
def slow(gen_a_start: int, gen_b_start: int) -> int:
    def generator(starting_value: int, factor: int, required_multiple: int) -> Generator[int, Any, NoReturn]:
        value = starting_value
        while True:
            value = (value * factor) % DIVISOR
            if value % required_multiple == 0:
                yield value

    gen_a = generator(gen_a_start, GEN_A_FACTOR, 4)
    gen_b = generator(gen_b_start, GEN_B_FACTOR, 8)

    num_matches = 0
    for _ in range(NUM_PAIRS):
        gen_a_value = next(gen_a)
        gen_b_value = next(gen_b)
        if gen_a_value & BIT_MASK == gen_b_value & BIT_MASK:
            num_matches += 1
    return num_matches


# 0.7 seconds
def with_numpy(gen_a_start: int, gen_b_start: int) -> int:
    def gen_values(start_value: int, factor: int, valid_mask: int) -> numpy.typing.NDArray[numpy.uint64]:
        values: numpy.typing.NDArray[numpy.uint64] = numpy.array(
            [(start_value * factor) % DIVISOR], numpy.uint64)
        valid_values = values[values & valid_mask == 0]
        while len(valid_values) < NUM_PAIRS:
            pow_factor = pow(factor, len(values), DIVISOR)
            new_values = (values * pow_factor) % DIVISOR
            values = numpy.concatenate([values, new_values])
            valid_values = numpy.concatenate([
                valid_values,
                new_values[new_values & valid_mask == 0][:(NUM_PAIRS - len(valid_values))]])
        return valid_values

    gen_a_values = gen_values(gen_a_start, GEN_A_FACTOR, 0b11)
    gen_b_values = gen_values(gen_b_start, GEN_B_FACTOR, 0b111)

    return ((gen_a_values & 0xffff) == (gen_b_values & 0xffff)).sum()


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        gen_a_start = int(input[0].split(' starts with ')[1])
        gen_b_start = int(input[1].split(' starts with ')[1])

        num_matches = with_numpy(gen_a_start, gen_b_start)

        log.log(log.RESULT, f'The number of matches seen by the judge: {num_matches}')
        return num_matches


part = Part1()

part.add_result(309, """
Generator A starts with 65
Generator B starts with 8921
""")

part.add_result(253)
