#!/usr/bin/python

from pathlib import Path

from shared import parse

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'


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
            print(prefix, 
                  f'For instruction {instruction} (r={r}, c={c}, b={b}), found bits for A of {a}:', 
                  ''.join(map(str, a_bits)))
            result = find_bits(remaining_instructions[:-1], bits_so_far + list(a_bits))
            if result is not None:
                return result
            else:
                print(prefix, 
                      f'Failed to find continuation for instruction {instruction} (r={r}, c={c}, b={b}), found bits for A of {a}:', 
                      ''.join(map(str, a_bits)))

    print(prefix, f'Failed to find instruction for {instruction}')
    return None    


def main():
    with INPUT_FILE.open() as ifp:
        state, program = parse(
                ifp.readlines()
            )

    bits = find_bits(program.instructions, [])

    if bits is None:
        print(f'Failed to find instructions for {program.instructions}')
    else:    
        a = to_num(tuple(bits))
        state.A = a
        program.execute(state)
        print('Program instructions are:\t\t', ','.join(map(str, program.instructions)))
        print('For A =', a, 'program output:\t', ','.join(map(str, state.out)))


if __name__ == '__main__':
    main()


"""
2,4  B = A % 8
1,3  B = B XOR 3
7,5  C = A // 2^B
1,5  B = B XOR 5
0,3  A = A // 8
4,2  B = B XOR C
5,5  print B % 8
3,0  Jump to 0

B = ((A % 8) XOR 3) XOR 5
C = A // 2^((A % 8) XOR 3)
A = A // 8
B = B XOR C
print B % 8


0,3  A = A // 8
5,4  print A % 8
3,0  Jump to 0

011 100 101 011 000 000

"""