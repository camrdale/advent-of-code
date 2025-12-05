from aoc.input import InputParser
from aoc import log
from aoc.range import Range
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        ranges_input, _ = parser.get_two_part_input()

        ranges = [Range.from_text(line) for line in ranges_input]

        merged_ranges: list[Range] = []

        for fresh_range in ranges:
            for merged_range in list(merged_ranges):
                merged_fresh_range = fresh_range.merge(merged_range)
                if merged_fresh_range is not None:
                    fresh_range = merged_fresh_range
                    merged_ranges.remove(merged_range)
            merged_ranges.append(fresh_range)

        num_fresh_ids = sum(fresh_range.length() for fresh_range in merged_ranges)

        log.log(log.RESULT, f'The total number of fresh ingredient IDs: {num_fresh_ids}')
        return num_fresh_ids


part = Part2()

part.add_result(14, """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
""")

part.add_result(339668510830757)
