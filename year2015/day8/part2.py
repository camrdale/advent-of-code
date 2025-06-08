from aoc.input import InputParser
from aoc import log
from aoc.runner import Part



class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        character_diff = 0
        for line in input:
            s = '"' + line.replace('\\', '\\\\').replace('"', '\\"') + '"'
            log.log(log.INFO, f'{line} -> {s}')
            character_diff += len(s) - len(line)

        log.log(log.RESULT, f'The difference in the number of characters: {character_diff}')
        return character_diff


part = Part2()

part.add_result(19, r"""
""
"abc"
"aaa\"aaa"
"\x27"
""")

part.add_result(2117)
