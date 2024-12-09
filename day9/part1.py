#!/usr/bin/python

from pathlib import Path

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'
TEST_INPUT = '2333133121414131402'

filemap: list[int] = []
with INPUT_FILE.open() as ifp:
    # text = TEST_INPUT
    text = ifp.readline().strip()
    filemap = list(map(int, text))

# print(filemap) 

blocks: list[int | None] = []

filelength = True
fileid = 0
for length in filemap:
    if filelength:
        filelength = False
        blocks.extend([fileid]*length)
        fileid += 1
    else:
        filelength = True
        blocks.extend([None]*length)

# print(blocks)

start_index = 0
end_index = len(blocks) - 1

while start_index < end_index:
    while start_index < end_index and blocks[start_index] is not None:
        start_index += 1
    while start_index < end_index and blocks[end_index] is None:
        end_index -= 1
    if start_index < end_index:
        blocks[end_index], blocks[start_index] = blocks[start_index], blocks[end_index]

# print(blocks)

checksum = 0
for i, fileid in enumerate(blocks):
    if fileid is None:
        break
    checksum += i * fileid

print('Checksum:', checksum)
