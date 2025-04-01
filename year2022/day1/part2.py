from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_multipart_input()

        total_calories = [sum(map(int, elf_calories)) for elf_calories in input]
        total_calories.sort(reverse=True)
        top_3_calories = sum(total_calories[:3])
        
        log.log(log.RESULT, f'Calories carried by the top 3 elves: {top_3_calories}')
        return top_3_calories


part = Part2()

part.add_result(45000, r"""
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

part.add_result(211189)
