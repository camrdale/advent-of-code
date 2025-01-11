import itertools

from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.map import ParsedMap
from aoc.runner import Part


def expand_input(input: list[str]) -> list[str]:
    expanded_input: list[str] = []
    for line in input:
        expanded_input.append(line)
        if all(c == '.' for c in line):
            expanded_input.append(line)
    return expanded_input


def transpose(input: list[str]) -> list[str]:
    transposed: list[str] = []
    for i in range(len(input[0])):
        transposed.append(''.join(line[i] for line in input))
    return transposed


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        input = expand_input(input)
        input = transpose(input)
        input = expand_input(input)
        input = transpose(input)

        map = ParsedMap(input, '#')
        galaxies = map.features['#']

        sum_path_lengths = 0
        for galaxy_1, galaxy_2 in itertools.combinations(galaxies, 2):
            offset = galaxy_1.difference(galaxy_2)
            sum_path_lengths += abs(offset.x) + abs(offset.y)

        log(RESULT, f'Sum of all the path lengths: {sum_path_lengths}')
        return sum_path_lengths


part = Part1()

part.add_result(374, """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""")

part.add_result(10422930)
