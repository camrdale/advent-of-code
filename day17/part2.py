from aoc.input import InputParser
from aoc.log import log, RESULT, INFO, DEBUG
from aoc.runner import Part

from .shared import parse


def to_bits(num: int) -> tuple[int, int, int]:
    return (
        1 if (num & 4) else 0,
        1 if (num & 2) else 0,
        1 if (num & 1) else 0
        )

def to_num(bits: tuple[int, ...]) -> int:
    out = 0
    for bit in bits:
        out = (out << 1) | bit
    return out


def right_shift(bits: list[int], r: int) -> tuple[int, int, int]:
    return (
        bits[-(r+3)] if r+2 < len(bits) else 0,
        bits[-(r+2)] if r+1 < len(bits) else 0,
        bits[-(r+1)] if r < len(bits) else 0,
    )


def find_bits(remaining_instructions: list[int], bits_so_far: list[int]) -> list[int] | None:
    if len(remaining_instructions) == 0:
        return bits_so_far
    
    prefix = '  '*(len(bits_so_far)//3)
    instruction = remaining_instructions[-1]
    for a in range(8):
        a_bits = to_bits(a)
        r = a ^ 3
        c = to_num(right_shift(bits_so_far + list(a_bits), r))
        b = r ^ 5
        if (b ^ c) == instruction:
            log(DEBUG,
                prefix, 
                f'For instruction {instruction} (r={r}, c={c}, b={b}), found bits for A of {a}:', 
                ''.join(map(str, a_bits)))
            result = find_bits(remaining_instructions[:-1], bits_so_far + list(a_bits))
            if result is not None:
                return result
            else:
                log(DEBUG,
                    prefix, 
                    f'Failed to find continuation for instruction {instruction} (r={r}, c={c}, b={b}), found bits for A of {a}:', 
                    ''.join(map(str, a_bits)))

    log(DEBUG, prefix, f'Failed to find instruction for {instruction}')
    return None    


class Part2(Part):
    def run(self, parser: InputParser) -> int | None:
        state, program = parse(parser.get_input())

        bits = find_bits(program.instructions, [])

        if bits is None:
            log(INFO, f'Failed to find instructions for {program.instructions}')
        else:
            a = to_num(tuple(bits))
            state.A = a
            program.execute(state)
            log(INFO, 'Program instructions are:\t\t', ','.join(map(str, program.instructions)))
            log(RESULT, 'For A =', a, 'program output:\t', ','.join(map(str, state.out)))
            return a


part = Part2()

part.add_result(216584205979245)
