#!/usr/bin/python

from pathlib import Path

from shared import parse

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'
TEST_INPUT = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""


def main():
    with INPUT_FILE.open() as ifp:
        state, program = parse(
                # TEST_INPUT.split('\n')
                ifp.readlines()
            )

    program.execute(state)

    print('Program output:', ','.join(map(str, state.out)))


if __name__ == '__main__':
    main()
