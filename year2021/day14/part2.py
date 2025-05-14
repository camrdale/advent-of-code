from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2021.day14.shared import PolymerConstructor


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        polymer_template_input, pair_insertion_rules_input = parser.get_two_part_input()

        constructor = PolymerConstructor(pair_insertion_rules_input)

        created = constructor.most_minus_least_letters(polymer_template_input[0], 40)

        log.log(log.RESULT, 'Most common minus the least common counts:', created)
        return created


part = Part2()

part.add_result(2188189693529, """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
""")

part.add_result(3459822539451)
