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

horizontal = [input[i:i+width] for i in range(0, height*width, width)]
vertical = [input[i:height*width:width] for i in range(0, width)]
diagonal_right = (
    [input[i:(height-i)*width:width+1] for i in range(1, width)]
    + [input[i:height*width:width+1] for i in range(0, height*width, width)])
diagonal_left = (
    [input[i:(i+1)*width-1:width-1] for i in range(0, width)]
    + [input[i:height*width:width-1] for i in range(2*width-1, height*width, width)])

def num_xmases(line: str) -> int:
    count = 0
    for i in range(len(line) - 3):
        if line[i:i+4] == 'XMAS' or line[i:i+4] == 'SAMX':
            count += 1
    return count

print('Number of XMASes:',
      sum([num_xmases(line) for line in horizontal + vertical + diagonal_left + diagonal_right]))
