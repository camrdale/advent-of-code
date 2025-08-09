import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()[0]

        input = re.sub(r'!.', '', input)
        log.log(log.INFO, f'Canceled removed:', input)

        garbage_removed = len(input)
        input = re.sub(r'<[^>]*>', '<>', input)
        log.log(log.INFO, f'Garbage removed:', input)

        # Garbage removed is length before - length after
        garbage_removed -= len(input)

        log.log(log.RESULT, f'The total garbage removed: {garbage_removed}')
        return garbage_removed


part = Part2()

part.add_result(0, """
{<>}
""")

part.add_result(17, """
{<random characters>}
""")

part.add_result(3, """
{<<<<>}
""")

part.add_result(2, """
{<{!>}>}
""")

part.add_result(0, """
{<!!>}
""")

part.add_result(0, """
{<!!!>>}
""")

part.add_result(10, """
{<{o"i!a,<{i<a>}
""")

part.add_result(6569)
