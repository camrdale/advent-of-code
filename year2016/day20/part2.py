from aoc.input import InputParser
from aoc import log
from aoc.range import Range, Ranges
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        firewall = Ranges()
        for line in input:
            firewall.add(Range.from_text(line))

        blocked = sum(range.length() for range in firewall)
        unblocked = 4294967295 + 1 - blocked

        log.log(log.RESULT, f'The number of IPs that are not blocked: {unblocked}')
        return unblocked


part = Part2()

part.add_result(117)
