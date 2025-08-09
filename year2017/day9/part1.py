import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()[0]

        input = re.sub(r'!.', '', input)
        log.log(log.INFO, f'Canceled removed:', input)

        input = re.sub(r'<[^>]*>', '', input)
        log.log(log.INFO, f'Garbage removed:', input)

        depth = 0
        total_score = 0
        for c in input:
            if c == '{':
                depth += 1
                total_score += depth
            elif c == '}':
                depth -= 1

        log.log(log.RESULT, f'The total score of all groups is: {total_score}')
        return total_score


part = Part1()

part.add_result(1, """
{}
""")

part.add_result(6, """
{{{}}}
""")

part.add_result(5, """
{{},{}}
""")

part.add_result(16, """
{{{},{},{{}}}}
""")

part.add_result(1, """
{<a>,<a>,<a>,<a>}
""")

part.add_result(9, """
{{<ab>},{<ab>},{<ab>},{<ab>}}
""")

part.add_result(9, """
{{<!!>},{<!!>},{<!!>},{<!!>}}
""")

part.add_result(3, """
{{<a!>},{<a!>},{<a!>},{<ab>}}
""")

part.add_result(14212)
