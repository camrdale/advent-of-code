#!/usr/bin/python

from collections import Counter
from pathlib import Path

import os, sys; sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from aoc.input import InputParser
from aoc.log import log, RESULT, set_log_level
from aoc.runner import Part

# Constants to represent the segments.
TOP = 'top'
MIDDLE = 'middle'
BOTTOM = 'bottom'
TOP_LEFT = 'top-left'
TOP_RIGHT = 'top-right'
BOTTOM_LEFT = 'bottom-left'
BOTTOM_RIGHT = 'bottom-right'

# Segments that make up each number.
ZERO = frozenset([TOP, BOTTOM, TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT])
ONE = frozenset([TOP_RIGHT, BOTTOM_RIGHT])
TWO = frozenset([TOP, MIDDLE, BOTTOM, TOP_RIGHT, BOTTOM_LEFT])
THREE = frozenset([TOP, MIDDLE, BOTTOM, TOP_RIGHT, BOTTOM_RIGHT])
FOUR = frozenset([MIDDLE, TOP_LEFT, TOP_RIGHT, BOTTOM_RIGHT])
FIVE = frozenset([TOP, MIDDLE, BOTTOM, TOP_LEFT, BOTTOM_RIGHT])
SIX = frozenset([TOP, MIDDLE, BOTTOM, TOP_LEFT, BOTTOM_LEFT, BOTTOM_RIGHT])
SEVEN = frozenset([TOP, TOP_RIGHT, BOTTOM_RIGHT])
EIGHT = frozenset([TOP, MIDDLE, BOTTOM, TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT])
NINE = frozenset([TOP, MIDDLE, BOTTOM, TOP_LEFT, TOP_RIGHT, BOTTOM_RIGHT])

# Mapping of number constants to numeric values.
NUMBERS = {ZERO: '0', ONE: '1', TWO: '2', THREE: '3', FOUR: '4', FIVE: '5', SIX: '6', SEVEN: '7', EIGHT: '8', NINE: '9'}


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        output_sum = 0

        for line in input:
            words = [frozenset(word) for word in line.split(' ')]
            patterns = words[0:10]
            output = words[11:15]

            # Count of the occurrences of each segment character in the patterns.
            segments: Counter[str] = Counter()
            for word in patterns:
                segments.update([c for c in word])
        
            # Mapping of digits to the set of segments that make them.
            mapping: dict[str, str] = {}
            # Mapping of the set of segments to the digit they make.
            reverse_mapping: dict[str, str] = {}

            # Initialize with the obvious ones based on length.
            top_and_top_right: list[str] = []
            for segment, count in segments.items():
                if count == 4:
                    mapping[BOTTOM_LEFT] = segment
                    reverse_mapping[segment] = BOTTOM_LEFT
                if count == 6:
                    mapping[TOP_LEFT] = segment
                    reverse_mapping[segment] = TOP_LEFT
                if count == 9:
                    mapping[BOTTOM_RIGHT] = segment
                    reverse_mapping[segment] = BOTTOM_RIGHT
                if count == 8:
                    top_and_top_right.append(segment)

            # Count of the occurrences of each segment character in the patterns that include TOP_LEFT.
            segments = Counter()
            for word in patterns:
                if mapping[TOP_LEFT] in word:
                    segments.update([c for c in word])

            # In numbers that include TOP_LEFT (0,4,5,6,8,9), the only unknown mapping that has 4 occurrences is TOP_RIGHT.
            for segment, count in segments.items():
                if segment not in reverse_mapping and count == 4:
                    mapping[TOP_RIGHT] = segment
                    reverse_mapping[segment] = TOP_RIGHT

            # That reveals TOP as the only other segment that appears in 8 numbers.
            segment = [s for s in top_and_top_right if s != mapping[TOP_RIGHT]][0]
            mapping[TOP] = segment
            reverse_mapping[segment] = TOP

            # Count of the occurrences of each segment character in the patterns that include BOTTOM_LEFT.
            segments = Counter()
            for word in patterns:
                if mapping[BOTTOM_LEFT] in word:
                    segments.update([c for c in word])

            # In numbers that include BOTTOM_LEFT (0,2,6,8), of the unknown mappings, MIDDLE has 3 occurrences and BOTTOM has 4.
            for segment, count in segments.items():
                if segment not in reverse_mapping and count == 3:
                    mapping[MIDDLE] = segment
                    reverse_mapping[segment] = MIDDLE
                if segment not in reverse_mapping and count == 4:
                    mapping[BOTTOM] = segment
                    reverse_mapping[segment] = BOTTOM

            output_sum += int(''.join(NUMBERS[frozenset(reverse_mapping[segment] for segment in word)] for word in output))

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
