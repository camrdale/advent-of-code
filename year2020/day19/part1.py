import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day19.shared import Rule


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        rule_input, message_input = parser.get_two_part_input()

        rules: dict[int, Rule] = {}
        for line in rule_input:
            rule = Rule(line)
            rules[rule.num] = rule
        
        regex = rules[0].regex(rules)
        log.log(log.INFO, regex)
        valid = re.compile(regex)

        num_valid = 0
        for line in message_input:
            match = valid.fullmatch(line)
            if match is not None:
                num_valid += 1

        log.log(log.RESULT, f'The number of meesages that match rule 0: {num_valid}')
        return num_valid


part = Part1()

part.add_result(2, """
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
""")

part.add_result(239)
