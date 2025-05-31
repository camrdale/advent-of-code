from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        floor = 0
        position = 0        
        for c in input[0]:
            position += 1
            match c:
                case '(':
                    floor += 1
                case ')':
                    floor -= 1
                case _:
                    raise ValueError(f'Unexpected input character: "{c}"')
            if floor < 0:
                break

        log.log(log.RESULT, f'The position of the character that causes Santa to first enter the basement: {position}')
        return position


part = Part2()

part.add_result(1, """
)
""")

part.add_result(5, """
()())
""")

part.add_result(1771)
