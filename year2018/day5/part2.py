import string

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day5.shared import react


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()[0]

        polymer = react(input)
        shortest_polymer = len(polymer)
        removed_unit = ''
        for c in string.ascii_lowercase:
            reduced = len(react(polymer.replace(c, '').replace(c.upper(), '')))
            if reduced < shortest_polymer:
                shortest_polymer = reduced
                removed_unit = c

        log.log(log.RESULT, f'Removing {removed_unit} makes a polymer of length: {shortest_polymer}')
        return shortest_polymer


part = Part2()

part.add_result(4, """
dabAcCaCBAcCcaDA
""")

part.add_result(6918)
