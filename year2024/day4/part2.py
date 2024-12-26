from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part


class Part2(Part):
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

        count = 0
        for i in range(len(input) - 2*width):
            if i % width not in (width - 1, width - 2):
                candidate = input[i] + input[i+2] + input[i+width+1] + input[i+2*width] + input[i+2*width+2]
                if candidate in ('MSAMS', 'MMASS', 'SMASM', 'SSAMM'):
                    count += 1

        log(RESULT, 'Number of X-MASes:', count)
        return count


part = Part2()

part.add_result(9, """
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

part.add_result(1902)
