from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        valid = 0
        for line in input:
            words = line.split()
            if len(set(words)) == len(words):
                valid += 1

        log.log(log.RESULT, f'The number of valid passphrases: {valid}')
        return valid


part = Part1()

part.add_result(2, """
aa bb cc dd ee
aa bb cc dd aa
aa bb cc dd aaa
""")

part.add_result(455)
