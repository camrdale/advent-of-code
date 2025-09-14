from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()
        num_recipes = int(input[0])

        N = num_recipes + 10

        recipes = [1]*(N + 1)
        recipes[0:2] = [3, 7]
        length = 2
        elf1 = 0
        elf2 = 1
        while length < N:
            recipe = recipes[elf1] + recipes[elf2]
            if recipe > 9:
                length += 1
            recipes[length] = recipe % 10
            length += 1
            elf1 = (elf1 + recipes[elf1] + 1) % length
            elf2 = (elf2 + recipes[elf2] + 1) % length
        
        next_ten = ''.join(map(str, recipes[num_recipes:N]))
        log.log(log.RESULT, f'The next ten recipes after {num_recipes}: {next_ten}')
        return next_ten


part = Part1()

part.add_result('5158916779', '9')

part.add_result('0124515891', '5')

part.add_result('9251071085', '18')

part.add_result('5941429882', '2018')

part.add_result('1052903161', '440231')
