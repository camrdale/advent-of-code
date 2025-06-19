import collections

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


def elementize(molecule: str) -> list[str]:
    elements: list[str] = []

    i = 0
    while i < len(molecule):
        if i + 1 < len(molecule) and molecule[i + 1].islower():
            elements.append(molecule[i:i+2])
            i += 2
        else:
            elements.append(molecule[i])
            i += 1

    return elements


def replacement_molecules(molecule: str, replacements: dict[str, list[str]]) -> set[str]:
    elements = elementize(molecule)

    molecules: set[str] = set()
    for i in range(len(elements)):
        for replacement in replacements[elements[i]]:
            molecules.add(''.join(elements[:i]) + replacement + ''.join(elements[i+1:]))
    
    return molecules


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        replacements_input, molecule_input = parser.get_two_part_input()

        replacements: dict[str, list[str]] = collections.defaultdict(list)
        for line in replacements_input:
            before, after = line.split(' => ')
            replacements[before].append(after)

        molecules = replacement_molecules(molecule_input[0], replacements)

        log.log(log.RESULT, f'The number of distinct molecules: {len(molecules)}')
        return len(molecules)


part = Part1()

part.add_result(4, """
H => HO
H => OH
O => HH

HOH
""")

part.add_result(7, """
H => HO
H => OH
O => HH

HOHOHO
""")

part.add_result(535)
