from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part

from year2023.day12.shared import possible_arrangements


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        total_possibilities = 0
        for line in input:
            record, damaged_groups_input = line.split()

            expanded_record = '?'.join([record]*5)
            expanded_damaged_groups_input = ','.join([damaged_groups_input]*5)

            damaged_groups = tuple(map(int, expanded_damaged_groups_input.split(',')))
            possibilities = possible_arrangements(expanded_record, damaged_groups)
            log(INFO, f'{expanded_record} {expanded_damaged_groups_input} - {possibilities} arrangements')
            total_possibilities += possibilities

        log(RESULT, f'Sum of all the path lengths: {total_possibilities}')
        return total_possibilities


part = Part2()

part.add_result(525152, """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
""")

part.add_result(7139671893722)
