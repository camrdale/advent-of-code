import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


BRACKETS = re.compile(r'[\[\]]')
ABA = re.compile(r'(.)(?!\1)(.)\1')


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        ssl = 0
        for line in input:
            parts = BRACKETS.split(line)
            assert len(parts) % 2 == 1, line

            abas: set[str] = set()
            inverse_babs: set[str] = set()
            for i, part in enumerate(parts):
                start = 0
                while match := ABA.search(part, start):
                    if i % 2 == 0:
                        abas.add(match.group(1) + match.group(2) + match.group(1))
                    else:
                        inverse_babs.add(match.group(2) + match.group(1) + match.group(2))
                    start = match.start() + 1

            if abas.intersection(inverse_babs):
                ssl += 1
            
        log.log(log.RESULT, f'The number of IPs that support SSL: "{ssl}"')
        return ssl


part = Part1()

part.add_result(3, """
aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb
""")

part.add_result(231)
