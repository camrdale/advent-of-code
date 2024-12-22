from aoc.input import InputParser
from aoc.log import log, RESULT, DEBUG, INFO
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        filemap = list(map(int, input[0]))

        log(DEBUG, filemap)

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

        log(DEBUG, blocks)

        start_index = 0
        end_index = len(blocks) - 1

        while start_index < end_index:
            while start_index < end_index and blocks[start_index] is not None:
                start_index += 1
            while start_index < end_index and blocks[end_index] is None:
                end_index -= 1
            if start_index < end_index:
                blocks[end_index], blocks[start_index] = blocks[start_index], blocks[end_index]

        log(INFO, blocks)

        checksum = 0
        for i, fileid in enumerate(blocks):
            if fileid is None:
                break
            checksum += i * fileid

        log(RESULT, 'Checksum:', checksum)
        return checksum


part = Part1()

part.add_result(1928, """
2333133121414131402
""")

part.add_result(6448989155953)
