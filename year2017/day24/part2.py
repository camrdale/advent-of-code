import functools

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day24.shared import Component


@functools.cache
def longest_strongest(from_port: int, remaining_components: frozenset[Component]) -> tuple[int, int]:
    max_bridge = (0, 0)
    for c in remaining_components:
        if from_port in c:
            length, strength = longest_strongest(c.other_port(from_port), remaining_components - {c})
            if (length + 1, c.strength() + strength) > max_bridge:
                max_bridge = (length + 1, c.strength() + strength)
    return max_bridge


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        components: set[Component] = set()
        for line in input:
            components.add(Component.from_text(line))

        max_length, max_strength = longest_strongest(0, frozenset(components))

        log.log(log.RESULT, f'The strongest bridge that can be built is length {max_length} and has strength: {max_strength}')
        return max_strength


part = Part1()

part.add_result(19, """
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
""")

part.add_result(1824)
