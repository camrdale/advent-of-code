from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        valid = 0
        for line in input:
            sorted_words = [''.join(sorted(word)) for word in line.split()]
            if len(set(sorted_words)) == len(sorted_words):
                valid += 1

        log.log(log.RESULT, f'The number of valid passphrases: {valid}')
        return valid


part = Part2()

part.add_result(3, """
abcde fghij
abcde xyz ecdab
a ab abc abd abf abj
iiii oiii ooii oooi oooo
oiii ioii iioi iiio
""")

part.add_result(186)
