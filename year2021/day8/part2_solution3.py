#!/usr/bin/python

import itertools
from pathlib import Path

import os, sys; sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from aoc.input import InputParser
from aoc.log import log, RESULT, set_log_level
from aoc.runner import Part

# Reference mapping of segment sets to corresponding numbers.
REFERENCE = {
    frozenset('acedgfb'): '8', frozenset('cdfbe'): '5', frozenset('gcdfa'): '2', frozenset('fbcad'): '3', 
    frozenset('dab'): '7', frozenset('cefabd'): '9', frozenset('cdfgeb'): '6', frozenset('eafb'): '4',
    frozenset('cagedb'): '0', frozenset('ab'): '1'}
# A set of all the 10 segment sets.
REFERENCE_SET = set(REFERENCE.keys())
# A randomly chosen ordering to represent the segments.
REFERENCE_SEGMENTS = 'acedgfb'


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        output_sum = 0

        for line in input:
            words = [frozenset(word) for word in line.split(' ')]
            patterns = words[0:10]
            output = words[11:15]

            # Try all possible permutations of the 7 segments.
            for possibility in itertools.permutations(REFERENCE_SEGMENTS):
                # Create a mapping from the permutation to the reference segment.
                mapping = dict(zip(possibility, REFERENCE_SEGMENTS))
                # Use the mapping to try to convert the patterns to the reference segment sets.
                mapped_patterns = set(frozenset(mapping[c] for c in pattern) for pattern in patterns)
                # If the resutl is the reference, then the mapping works.
                if mapped_patterns == REFERENCE_SET:
                    # Use the mapping to convert the outputs to the reference, then to the digits they represent.
                    output_sum += int(''.join(REFERENCE[frozenset(mapping[c] for c in word)] for word in output))
                    break

        log(RESULT, 'total sum of output:', output_sum)
        return output_sum


part = Part2()

part.add_result(61229, """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""")

part.add_result(1016804)


if __name__ == '__main__':
    set_log_level(RESULT)
    assert part.run_part(2021, 8, 2, subdirectory=Path(sys.argv[0]))
