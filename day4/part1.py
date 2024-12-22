from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        raw_input = parser.get_input()

        width = 0
        height = 0
        input: str = ''
        for text in raw_input:
            if width != 0 and len(text) != width:
                print('ERROR input is mangled')
                return -1
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

        xmases_appear = sum([num_xmases(line) for line in horizontal + vertical + diagonal_left + diagonal_right])
        log(RESULT, 'Number of XMASes:', xmases_appear)
        return xmases_appear


part = Part1()

part.add_result(18, """
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
""")

part.add_result(2562)
