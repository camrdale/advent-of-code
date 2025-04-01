from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_multipart_input()

        most_calories = 0
        for elf_calories in input:
            calories = sum(map(int, elf_calories))
            most_calories = max(most_calories, calories)
        
        log.log(log.RESULT, f'Most calories carried by an elf: {most_calories}')
        return most_calories


part = Part1()

part.add_result(24000, r"""
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
""")

part.add_result(71471)
