#!/usr/bin/python

from pathlib import Path
import re

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'

MUL_PATTERN = re.compile(r'mul\(([0-9]*),([0-9]*)\)')

input: list[str] = []
with INPUT_FILE.open() as ifp:
    while True:
        c = ifp.read(1)
        if not c:
            break
        if c == 'm':
            input.append('')
        if len(input) == 0:
            continue
        input[-1] += c

multiplications = 0
for mul in input:
    match = MUL_PATTERN.match(mul)
    if match is None:
        continue
    (l, r) = match.group(1,2)
    multiplications += int(l) * int(r)

print('Results of the multiplications:', multiplications)
