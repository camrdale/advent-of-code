from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        floor = 0
        for c in input[0]:
            match c:
                case '(':
                    floor += 1
                case ')':
                    floor -= 1
                case _:
                    raise ValueError(f'Unexpected input character: "{c}"')

        log.log(log.RESULT, f'Santa ends up on floor: {floor}')
        return floor


part = Part1()

part.add_result(0, """
(())
""")

part.add_result(0, """
()()
""")

part.add_result(3, """
(((
""")

part.add_result(3, """
(()(()(
""")

part.add_result(3, """
))(((((
""")

part.add_result(-1, """
())
""")

part.add_result(-1, """
))(
""")

part.add_result(-3, """
)))
""")

part.add_result(-3, """
)())())
""")

part.add_result(138)
