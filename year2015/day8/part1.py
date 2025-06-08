from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        character_diff = 0
        for line in input:
            s = bytes(line[1:-1], 'ascii').decode('unicode_escape')
            log.log(log.INFO, f'{line} -> {s}')
            character_diff += len(line) - len(s)

        log.log(log.RESULT, f'The difference in the number of characters: {character_diff}')
        return character_diff


part = Part1()

part.add_result(12, r"""
""
"abc"
"aaa\"aaa"
"\x27"
""")

part.add_result(1371)
