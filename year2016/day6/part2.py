import collections

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()

        counters: list[collections.Counter[str]] = [collections.Counter() for _ in range(len(input[0]))]

        for line in input:
            for i, c in enumerate(line):
                counters[i][c] += 1

        message = ''.join(counter.most_common()[-1][0] for counter in counters)
            
        log.log(log.RESULT, f'The error-corrected message is: "{message}"')
        return message


part = Part2()

part.add_result('advent', """
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
""")

part.add_result('jucfoary')
