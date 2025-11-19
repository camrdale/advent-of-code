import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day19.shared import Rule


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        rule_input, message_input = parser.get_two_part_input()

        rules: dict[int, Rule] = {}
        for line in rule_input:
            rule = Rule(line)
            rules[rule.num] = rule

        rule_42 = rules[42].regex(rules)
        rule_31 = rules[31].regex(rules)

        rule_0s: list[re.Pattern[str]] = []
        for i in range(2, 7):
            for j in range(1, i):
                # Rule 0 must match some number of rule 42s, followed by some smaller number of rule 31s
                rule_0s.append(re.compile(rule_42*i + rule_31*j))

        num_valid = 0
        for line in message_input:
            for regex in rule_0s:
                if regex.fullmatch(line) is not None:
                    num_valid += 1
                    break

        log.log(log.RESULT, f'The number of meesages that match rule 0: {num_valid}')
        return num_valid


part = Part2()

part.add_result(12, """
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
""")

part.add_result(405)
