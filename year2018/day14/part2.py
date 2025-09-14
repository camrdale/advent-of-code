from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        score_sequence = list(map(int, input[0]))
        n = len(score_sequence)

        N = int(input[0])

        recipes = [1]*(N + 1)
        recipes[0:2] = [3, 7]
        length = 2
        elf1 = 0
        elf2 = 1
        while True:
            if length + 2 > len(recipes):
                recipes.extend([1]*(N + 1))
            recipe = recipes[elf1] + recipes[elf2]
            if recipe > 9:
                length += 1
                if recipes[length-n:length] == score_sequence:
                    break
            recipes[length] = recipe % 10
            length += 1
            if recipes[length-n:length] == score_sequence:
                break
            elf1 = (elf1 + recipes[elf1] + 1) % length
            elf2 = (elf2 + recipes[elf2] + 1) % length
        
        log.log(log.RESULT, f'The score sequence {score_sequence} appears after recipe: {length - n}')
        return length - n


part = Part1()

part.add_result(9, '51589')

part.add_result(5, '01245')

part.add_result(18, '92510')

part.add_result(2018, '59414')

part.add_result(20165504, '440231')
