#!/usr/bin/python

from pathlib import Path

from shared import RobotMap

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'
TEST_INPUT = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""


def main():
    with INPUT_FILE.open() as ifp:
        robots = RobotMap(
                # TEST_INPUT.split('\n'), 11, 7
                ifp.readlines(), 101, 103
                )
        
    # print(robots)

    robots.simulate(100)

    # print(robots)

    print('Safety factor after 100s:', robots.safety_factor())


if __name__ == '__main__':
    main()
