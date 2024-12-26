#!/usr/bin/python

from collections import Counter
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
# Count of the occurrences of each segment character in the patterns.
REFERENCE_SEGMENTS = Counter([c for word in REFERENCE for c in word])
# Scores (sum of the total counts of the occurrences of the segments)
# for the reference segment sets, mapped to their numbers.
REFERENCE_SCORES = dict(
    (sum(REFERENCE_SEGMENTS[c] for c in word), REFERENCE[word])
    for word in REFERENCE)


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        output_sum = 0

        for line in input:
            words = [frozenset(word) for word in line.split(' ')]
            patterns = words[0:10]
            output = words[11:15]

            # Count of the occurrences of each segment character in the patterns.
            segments = Counter([c for word in patterns for c in word])

            # Calculate the score for each pattern, and map that to the corresponding number
            # using the reference scores.
            mapping = dict(
                (word, REFERENCE_SCORES[sum(segments[c] for c in word)])
                for word in patterns)

            output_sum += int(''.join([mapping[word] for word in output]))

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
