#!/usr/bin/python

from collections import defaultdict
import itertools
from pathlib import Path

from shared import Offset, Node

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'
TEST_INPUT = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


nodes: dict[str, list[Node]] = defaultdict(list)

height = 0
width = 0
with INPUT_FILE.open() as ifp:
    # for y, line in enumerate(TEST_INPUT.split()):
    for y, line in enumerate(ifp.readlines()):
        if len(line.strip()) > 0:
            width = len(line.strip())
            height += 1
            for x, c in enumerate(line.strip()):
                if c == '.':
                    continue
                nodes[c].append(Node(x,y))

# print(width, height)
# print(nodes)

antinodes: set[Node] = set()
for typednodes in nodes.values():
    for node1, node2 in itertools.combinations(typednodes, 2):
        offset: Offset = node2.difference(node1)
        antinode2 = node2.add(offset)
        if antinode2.valid(width, height):
            # print(node1, node2, antinode2)
            antinodes.add(antinode2)
        antinode1 = node1.add(offset.negate())
        if antinode1.valid(width, height):
            # print(node2, node1, antinode1)
            antinodes.add(antinode1)

# print(antinodes)

print('Unique antinode locations:', len(antinodes))
