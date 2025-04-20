from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day20.shared import EncryptedFile


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        encrypted_file = EncryptedFile(input, decryption_key=811589153)
        log.log(log.INFO, encrypted_file)

        for i in range(10):
            encrypted_file.mix()
            log.log(log.INFO, f'After {i+1} rounds of mixing: {encrypted_file}')

        coordinates = encrypted_file.grove_coordinates()
        log.log(log.INFO, f'The 1000th, 2000th and 3000th numbers after 0 are: {coordinates}')
        
        log.log(log.RESULT, f'The sum of the threee coordinate numbers are: {sum(coordinates)}')
        return sum(coordinates)


part = Part2()

part.add_result(1623178306, r"""
1
2
-3
3
-2
0
4
""")

part.add_result(1632917375836)
