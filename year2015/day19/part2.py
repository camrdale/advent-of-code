import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        replacements_input, molecule_input = parser.get_two_part_input()

        # Replacements to work backwards from the target molecule to the starting one.
        replacements: dict[str, str] = {}
        for line in replacements_input:
            before, after = line.split(' => ')
            assert after not in replacements, f'Found duplicate for {after}: {replacements[after]}, {before}'
            replacements[after] = before

        replacement_regex = re.compile('(' + '|'.join(replacements.keys()) + ')')

        molecule = molecule_input[0]
        steps = 0
        while molecule != 'e':
            match = replacement_regex.search(molecule)
            if match is None:
                raise ValueError(f'Failed to find a replacement in: {molecule}')
            
            # Find the last match in the molecule.
            last_match = match
            while match := replacement_regex.search(molecule, last_match.start(1) + 1):
                last_match = match
            
            molecule = molecule[:last_match.start(1)] + replacements[last_match.group(1)] + molecule[last_match.end(1):]
            steps += 1

        log.log(log.RESULT, f'The fewest number of steps to get the target molecule: {steps}')
        return steps


part = Part2()

part.add_result(212)
