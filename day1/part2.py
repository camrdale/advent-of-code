#!/usr/bin/python

from pathlib import Path
from collections import defaultdict

INPUT_FILE = Path('input.txt')

left_input: list[int] = []
right_input: dict[int, int] = defaultdict(int)
with INPUT_FILE.open() as ifp:
    for line in ifp.readlines():
        val = line.split()
        left_input.append(int(val[0]))
        right_input[int(val[1])] += 1

similarity_score = 0
for left in left_input:
    similarity_score += left * right_input[left]

print('Similarity Score:', similarity_score)
