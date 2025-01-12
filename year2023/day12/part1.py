from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part

from year2023.day12.shared import possible_arrangements


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        total_possibilities = 0
        for line in input:
            record, damaged_groups_input = line.split()

            damaged_groups = tuple(map(int, damaged_groups_input.split(',')))
            possibilities = possible_arrangements(record, damaged_groups)
            log(INFO, f'{record} {damaged_groups_input} - {possibilities} arrangements')
            total_possibilities += possibilities


        log(RESULT, f'Sum of all the path lengths: {total_possibilities}')
        return total_possibilities


part = Part1()

part.add_result(21, """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
""")

part.add_result(7221)
