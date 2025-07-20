from aoc.input import InputParser
from aoc import log
from aoc.range import Range, Ranges
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        firewall = Ranges()
        for line in input:
            firewall.add(Range.from_text(line))

        unblocked = 0
        for range in firewall:
            if range.start > unblocked:
                break
            unblocked = range.end + 1

        log.log(log.RESULT, f'The lowest-valued IP that is not blocked: {unblocked}')
        return unblocked


part = Part1()

part.add_result(3, """
5-8
0-2
4-7
""")

part.add_result(31053880)
