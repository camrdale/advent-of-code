#!/usr/bin/python

from pathlib import Path

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'
TEST_INPUT = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

width = 0
height = 0
input: str = ''
with INPUT_FILE.open() as ifp:
    # for line in TEST_INPUT.split():
    for line in ifp.readlines():
        text = line.strip()
        if width != 0 and len(text) != width:
            exit(1)
        width = len(text)
        input += text
        height += 1

count = 0
for i in range(len(input) - 2*width):
    if i % width not in (width - 1, width - 2):
        candidate = input[i] + input[i+2] + input[i+width+1] + input[i+2*width] + input[i+2*width+2]
        if candidate in ('MSAMS', 'MMASS', 'SMASM', 'SSAMM'):
            count += 1

print('Number of X-MASes:', count)
