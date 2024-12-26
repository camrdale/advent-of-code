from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        output_sum = 0

        for line in input:
            words = [frozenset(word) for word in line.split(' ')]
            patterns = words[0:10]
            output = words[11:15]

            # Mapping of digits to the set of segments that make them.
            mapping: dict[int, frozenset[str]] = {}
            # Mapping of the set of segments to the digit they make.
            reverse_mapping: dict[frozenset[str], int] = {}

            # Initialize with the obvious ones based on length.
            for word in patterns:
                if len(word) == 2:
                    mapping[1] = word
                    reverse_mapping[word] = 1
                if len(word) == 4:
                    mapping[4] = word
                    reverse_mapping[word] = 4
                if len(word) == 3:
                    mapping[7] = word
                    reverse_mapping[word] = 7
                if len(word) == 7:
                    mapping[8] = word
                    reverse_mapping[word] = 8

            # Union of 4 and 7 can only be a subset of 8 or 9.
            four_plus_seven = mapping[4].union(mapping[7])
            for word in patterns:
                if word == mapping[8]:
                    continue
                if four_plus_seven <= word:
                    reverse_mapping[word] = 9
                    mapping[9] = word

            # Remaining 6 length digits 0 and 6, 1 is a subset of 0 but not 6.
            for word in patterns:
                if len(word) == 6 and word != mapping[9]:
                    if mapping[1] <= word:
                        reverse_mapping[word] = 0
                        mapping[0] = word
                    else:
                        reverse_mapping[word] = 6
                        mapping[6] = word

            # Of 5 length digits (2,3,5), only 5 unioned with 7 gives 9.
            for word in patterns:
                if len(word) == 5:
                    if word.union(mapping[7]) == mapping[9]:
                        reverse_mapping[word] = 5
                        mapping[5] = word

            # Remaining 5 length digits 2 and 3, only 3 unioned with 5 gives 9.
            for word in patterns:
                if len(word) == 5 and word != mapping[5]:
                    if word.union(mapping[5]) == mapping[9]:
                        reverse_mapping[word] = 3
                        mapping[3] = word
                    else:
                        reverse_mapping[word] = 2
                        mapping[2] = word

            output_sum += int(''.join([str(reverse_mapping[word]) for word in output]))

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
