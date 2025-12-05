from aoc.input import InputParser
from aoc import log
from aoc.range import Range
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        ranges_input, ingredient_input = parser.get_two_part_input()

        ranges = [Range.from_text(line) for line in ranges_input]

        fresh = 0
        for ingredient in map(int, ingredient_input):
            for fresh_range in ranges:
                if fresh_range.contains_value(ingredient):
                    fresh += 1
                    break

        log.log(log.RESULT, f'The number of fresh ingredients: {fresh}')
        return fresh


part = Part1()

part.add_result(3, """
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

part.add_result(513)
