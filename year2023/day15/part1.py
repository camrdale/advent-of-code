from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part

from year2023.day15.shared import hash_function


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        sum_of_hashes = 0
        for step in input[0].split(','):
            hash_value = hash_function(step)
            log(INFO, f'{step} becomes {hash_value}')
            sum_of_hashes += hash_value

        log(RESULT, f'The sum of the hashes: {sum_of_hashes}')
        return sum_of_hashes


part = Part1()

part.add_result(52, """
HASH
""")

part.add_result(1320, """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
""")

part.add_result(519041)
