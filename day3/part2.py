#!/usr/bin/python

from pathlib import Path
import re

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'

MUL_PATTERN = re.compile(r'mul\(([0-9]*),([0-9]*)\)')
DO_PATTERN = re.compile(r'do\(\)')
DONT_PATTERN = re.compile(r'don\'t\(\)')

input: list[str] = []
with INPUT_FILE.open() as ifp:
    while True:
        c = ifp.read(1)
        if not c:
            break
        if c == 'm' or c == 'd':
            input.append('')
        if len(input) == 0:
            continue
        input[-1] += c

enabled = True
multiplications = 0
for command in input:
    if DO_PATTERN.match(command) is not None:
        enabled = True
        continue
    if DONT_PATTERN.match(command) is not None:
        enabled = False
        continue
    if enabled:
        match = MUL_PATTERN.match(command)
        if match is not None:
            (l, r) = match.group(1,2)
            multiplications += int(l) * int(r)

print('Results of the enabled multiplications:', multiplications)
