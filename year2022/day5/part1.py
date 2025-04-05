from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day5.shared import parse_stacks, parse_moves


class Part1(Part):
    def run(self, parser: InputParser) -> str:
        crates_input, moves_input = parser.get_two_part_input()
        crates = parse_stacks(crates_input)
        log.log(log.DEBUG, crates)

        for num_crates, from_stack, to_stack in parse_moves(moves_input):
            log.log(log.DEBUG, f'Move {num_crates} from {from_stack} to {to_stack}')
            crates[to_stack].extend(crates[from_stack][-1:-num_crates-1:-1])
            del crates[from_stack][-num_crates:]
            log.log(log.DEBUG, crates)
        
        top_crates = ''.join(crates[i][-1] for i in range(1, max(crates) + 1))
        log.log(log.RESULT, f'The top crates on each stack are: {top_crates}')
        return top_crates


part = Part1()

part.add_result('CMZ', r"""
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""")

part.add_result('VJSFHWGFT')
