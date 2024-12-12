#!/usr/bin/python

from pathlib import Path

from shared import Garden

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'
TEST_INPUT = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

def main():
    with INPUT_FILE.open() as ifp:
        garden = Garden(
                # TEST_INPUT.split()
                ifp.readlines()
        )

    # print(garden)
    
    garden.merge()

    # print(garden)

    print('Total garden price:', garden.price())


if __name__ == '__main__':
    main()
