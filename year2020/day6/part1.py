from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_multipart_input()

        yes_counts = 0
        for group in input:
            questions: set[str] = set()

            for line in group:
                questions.update(line)

            yes_counts += len(questions)

        log.log(log.RESULT, f'The sum of the Yes counts of all the groups: {yes_counts}')
        return yes_counts


part = Part1()

part.add_result(11, """
abc

a
b
c

ab
ac

a
a
a
a

b
""")

part.add_result(6782)
