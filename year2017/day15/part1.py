import concurrent.futures
import sys

import numpy
import numpy.typing

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


GEN_A_FACTOR = 16807
GEN_B_FACTOR = 48271
DIVISOR = 2147483647
BIT_MASK = 0xFFFF
NUM_PAIRS = 40_000_000
BLOCK_SIZE = 100000


# 7 seconds
def slow(gen_a_start: int, gen_b_start: int) -> int:
    num_matches = 0
    gen_a = gen_a_start
    gen_b = gen_b_start
    for _ in range(NUM_PAIRS):
        gen_a = (gen_a * GEN_A_FACTOR) % DIVISOR
        gen_b = (gen_b * GEN_B_FACTOR) % DIVISOR
        if gen_a & BIT_MASK == gen_b & BIT_MASK:
            num_matches += 1
    return num_matches


# 5 seconds first run, 0.8 seconds on reruns
def parallelized(gen_a_start: int, gen_b_start: int) -> int:
    num_matches = 0

    def parallel_num_matches(start_i: int) -> int:
        num_matches = 0
        gen_a = (gen_a_start * pow(GEN_A_FACTOR, start_i, DIVISOR)) % DIVISOR
        gen_b = (gen_b_start * pow(GEN_B_FACTOR, start_i, DIVISOR)) % DIVISOR
        for _ in range(BLOCK_SIZE):
            gen_a = (gen_a * GEN_A_FACTOR) % DIVISOR
            gen_b = (gen_b * GEN_B_FACTOR) % DIVISOR
            if gen_a & BIT_MASK == gen_b & BIT_MASK:
                num_matches += 1
        return num_matches

    assert not sys._is_gil_enabled() # type: ignore
    with log.ProgressBar(NUM_PAIRS // BLOCK_SIZE, desc='day 15,1') as progress_bar:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures: list[concurrent.futures.Future[int]] = []
            for start_i in range(0, NUM_PAIRS, BLOCK_SIZE):
                futures.append(executor.submit(parallel_num_matches, start_i))
            for future in concurrent.futures.as_completed(futures):
                progress_bar.update()
                num_matches += future.result()

    return num_matches


# 0.5 seconds
def with_numpy(gen_a_start: int, gen_b_start: int) -> int:
    def gen_values(start_value: int, factor: int) -> numpy.typing.NDArray[numpy.uint64]:
        values: numpy.typing.NDArray[numpy.uint64] = numpy.array(
            [(start_value * factor) % DIVISOR], numpy.uint64)
        while len(values) < NUM_PAIRS:
            pow_factor = pow(factor, len(values), DIVISOR)
            values = numpy.concatenate([
                values,
                (values[:(NUM_PAIRS - len(values))] * pow_factor) % DIVISOR])
        return values

    gen_a_values = gen_values(gen_a_start, GEN_A_FACTOR)
    gen_b_values = gen_values(gen_b_start, GEN_B_FACTOR)

    return ((gen_a_values & BIT_MASK) == (gen_b_values & BIT_MASK)).sum()


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        gen_a_start = int(input[0].split(' starts with ')[1])
        gen_b_start = int(input[1].split(' starts with ')[1])

        num_matches = with_numpy(gen_a_start, gen_b_start)

        log.log(log.RESULT, f'The number of matches seen by the judge: {num_matches}')
        return num_matches


part = Part1()

part.add_result(588, """
Generator A starts with 65
Generator B starts with 8921
""")

part.add_result(609)
