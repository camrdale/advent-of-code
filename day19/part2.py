#!/usr/bin/python

from pathlib import Path

from shared import Towels

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'
TEST_INPUT = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""


def main():
    with INPUT_FILE.open() as ifp:
        input = (
            # TEST_INPUT.split('\n')
            ifp.readlines()
        )

    towels = Towels(input[0])

    # print(f'There are {len(towels.towels)} towels with max length {towels.max_length}')

    num_possible = 0    
    for design in input[1:]:
        if len(design.strip()) == 0:
            continue

        possible = towels.build_design(design.strip())
        # print(f'possible {possible} ways' if possible > 0 else 'NOT POSSIBLE', 'for design', design.strip())
        num_possible += possible

    print(f'Number of possible designs: {num_possible}')


if __name__ == '__main__':
    main()
