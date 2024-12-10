#!/usr/bin/python

from pathlib import Path

from shared import TopographicMap

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'
TEST_INPUT = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

def main():
    with INPUT_FILE.open() as ifp:
        map = TopographicMap(
                # TEST_INPUT.split()
                ifp.readlines()
        )

    trailhead_ratings = 0
    for trailhead in map.trailheads():
        rating = map.rating(trailhead)
        # print('Trailhead', trailhead, 'has a rating of', rating)
        trailhead_ratings += rating

    print('Total trailhead rating:', trailhead_ratings)


if __name__ == '__main__':
    main()
