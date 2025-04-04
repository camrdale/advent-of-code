from typing import NamedTuple

from aoc.input import InputParser
from aoc.log import log, RESULT, INFO, DEBUG
from aoc.range import Range
from aoc.runner import Part


class Conversion(NamedTuple):
    conversion_range: Range
    delta: int

    def apply(self, ranges: list[Range]) -> tuple[list[Range], list[Range]]:
        log(DEBUG, f'  Applying conversion {self} to {ranges}')
        affected_ranges: list[Range] = []
        unaffected_ranges: list[Range] = []
        for range in ranges:
            if not self.conversion_range.intersects(range):
                log(DEBUG, f'    Range {range} does not intersect {self.conversion_range}')
                unaffected_ranges.append(range)
                continue
            if self.conversion_range.start > range.start:
                unaffected_ranges.append(Range.open(range.start, self.conversion_range.start))
                log(DEBUG, f'    Split start from {range}: {unaffected_ranges[-1]}')
            if self.conversion_range.end < range.end:
                unaffected_ranges.append(Range.open(self.conversion_range.end, range.end))
                log(DEBUG, f'    Split end from {range}: {unaffected_ranges[-1]}')
            affected_range = Range.open(
                max(range.start, self.conversion_range.start),
                min(range.end, self.conversion_range.end))
            log(DEBUG, f'    {range} needs to be modified in: {affected_range}')
            delta_range = affected_range.offset(self.delta)
            log(DEBUG, f'    {range} results in new range: {delta_range}')
            affected_ranges.append(delta_range)
        return unaffected_ranges, affected_ranges


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        ranges: list[Range] = []
        seed_nums = list(map(int, input[0].split(':')[1].split()))
        for i in range(0, len(seed_nums), 2):
            start, range_length = seed_nums[i], seed_nums[i+1]
            ranges.append(Range.open(start, start + range_length))

        i = 3
        while i < len(input):
            log(INFO, ranges)
            new_ranges: list[Range] = []
            while i < len(input) and input[i] != '':
                destination_start, source_start, range_length = map(int, input[i].split())
                conversion = Conversion(Range.open(source_start, source_start + range_length), destination_start - source_start)
                ranges, affected_ranges = conversion.apply(ranges)
                new_ranges.extend(affected_ranges)
                i += 1
            ranges.extend(new_ranges)
            i += 2

        log(INFO, ranges)
        min_location = min(ranges)
        log(RESULT, f'The lowest location number range is: {min_location}')
        return min_location.start


part = Part2()

part.add_result(46, """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""")

part.add_result(63179500)
