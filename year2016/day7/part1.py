import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


BRACKETS = re.compile(r'[\[\]]')
ABBA = re.compile(r'(.)(?!\1)(.)\2\1')


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        tls = 0
        for line in input:
            parts = BRACKETS.split(line)
            assert len(parts) % 2 == 1, line

            if any([ABBA.search(parts[i]) for i in range(1, len(parts), 2)]):
                continue

            if any([ABBA.search(parts[i]) for i in range(0, len(parts), 2)]):
                tls += 1
            
        log.log(log.RESULT, f'The number of IPs that support TLS: "{tls}"')
        return tls


part = Part1()

part.add_result(2, """
abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
""")

part.add_result(115)
