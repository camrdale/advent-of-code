#!/usr/bin/python

from pathlib import Path
from typing import NamedTuple

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'
TEST_INPUT = '2333133121414131402'


class File(NamedTuple):
    id: int
    length: int


class FreeSpace(NamedTuple):
    length: int


class HardDrive:
    def __init__(self, filemap: list[int]):
        self.blocks: list[File | FreeSpace] = []
        filelength = True
        fileid = 0
        for length in filemap:
            if filelength:
                filelength = False
                self.blocks.append(File(fileid, length))
                fileid += 1
            else:
                filelength = True
                self.blocks.append(FreeSpace(length))

    def defrag(self):
        end_index = len(self.blocks) - 1
        while end_index > 0:
            file = self.blocks[end_index]
            if type(file) is not File:
                end_index -= 1
                continue
            for start_index in range(end_index):
                free_space = self.blocks[start_index]
                if type(free_space) is not FreeSpace:
                    continue
                if free_space.length >= file.length:
                    self.blocks[start_index] = file
                    self.blocks[end_index] = FreeSpace(file.length)
                    if free_space.length > file.length:
                        self.blocks.insert(start_index+1, FreeSpace(free_space.length - file.length))
                        end_index += 1
                    break
            end_index -= 1

    def checksum(self):
        checksum = 0
        position = 0
        for block in self.blocks:
            if type(block) is not File:
                position += block.length
                continue
            for i in range(block.length):
                checksum += (position + i) * block.id
            position += block.length
        return checksum


filemap: list[int] = []
with INPUT_FILE.open() as ifp:
    # text = TEST_INPUT
    text = ifp.readline().strip()
    filemap = list(map(int, text))

# print(filemap) 

hard_drive = HardDrive(filemap)

# print(hard_drive.blocks)

hard_drive.defrag()

# print(hard_drive.blocks)

print('Checksum:', hard_drive.checksum())