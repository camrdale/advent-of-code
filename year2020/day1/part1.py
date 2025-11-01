from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        entries = set(map(int, input))

        for entry in entries:
            if (2020 - entry) in entries:
                log.log(log.RESULT, f'The two entries that sum to 2020: {entry} * {2020 - entry} = {entry * (2020 - entry)}')
                return entry * (2020 - entry)
        
        raise ValueError(f'Failed to find two entries that sum to 2020')


part = Part1()

part.add_result(514579, """
1721
979
366
299
675
1456
""")

part.add_result(928896)
