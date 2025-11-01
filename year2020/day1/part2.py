import itertools

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        entries = set(map(int, input))

        for entry1, entry2 in itertools.combinations(entries, 2):
            if (2020 - entry1 - entry2) in entries:
                log.log(log.RESULT, f'The three entries that sum to 2020: {entry1} * {entry2} * {2020 - entry1 - entry2} = {entry1 * entry2 * (2020 - entry1 - entry2)}')
                return entry1 * entry2 * (2020 - entry1 - entry2)
        
        raise ValueError(f'Failed to find three entries that sum to 2020')


part = Part2()

part.add_result(241861950, """
1721
979
366
299
675
1456
""")

part.add_result(295668576)
