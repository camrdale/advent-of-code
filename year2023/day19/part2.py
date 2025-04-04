import re
from typing import NamedTuple

from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.range import Range
import aoc.runner

PART_PARSER = re.compile(r'{x=([0-9]*),m=([0-9]*),a=([0-9]*),s=([0-9]*)}')
RULE_PARSER = re.compile(r'([xmas])([<>])([0-9]*):(.*)')


class XmasRange(NamedTuple):
    x: Range
    m: Range
    a: Range
    s: Range

    def possible_combinations(self) -> int:
        return self.x.length() * self.m.length() * self.a.length() * self.s.length()
    
    def update(self, rating: str, new_range: Range|None) -> 'XmasRange | None':
        if new_range is not None:
            return self._replace(**{rating: new_range})
        return None


class Rule(NamedTuple):
    rating: str
    operator: str
    value: int
    result: str

    @classmethod
    def from_text(cls, rule_text: str) -> 'Rule | None':
        match = RULE_PARSER.match(rule_text)
        if match is not None:
            return cls(match.group(1), match.group(2), int(match.group(3)), match.group(4))
        return None

    def apply(self, ranges: XmasRange) -> tuple[XmasRange|None, str, XmasRange|None]:
        range = getattr(ranges, self.rating)

        range_true: XmasRange|None = None
        range_false: XmasRange|None = None
        if self.operator == '>':
            new_ranges = range.split(self.value + 1)
            range_true = ranges.update(self.rating, new_ranges[1])
            range_false = ranges.update(self.rating, new_ranges[0])
        else:
            new_ranges = range.split(self.value)
            range_true = ranges.update(self.rating, new_ranges[0])
            range_false = ranges.update(self.rating, new_ranges[1])
        return range_true, self.result, range_false


class Workflow:
    def __init__(self, rules: list[Rule], final_result: str):
        self.rules: list[Rule] = rules
        self.final_result = final_result

    def apply(self, ranges: XmasRange) -> list[tuple[XmasRange, str]]:
        results: list[tuple[XmasRange, str]] = []
        for rule in self.rules:
            range_true, result, range_false = rule.apply(ranges)
            if range_true is not None:
                results.append((range_true, result))
            if range_false is None:
                break
            ranges = range_false
        results.append((ranges, self.final_result))
        return results


class Part2(aoc.runner.Part):
    def run(self, parser: InputParser) -> int:
        workflow_input, _ = parser.get_two_part_input()

        workflows: dict[str, Workflow] = {}
        for line in workflow_input:
            name, rules_input = line.split('{')
            rules_text = rules_input[:-1].split(',')
            rules: list[Rule] = []
            final_result = ''
            for rule_text in rules_text:
                rule = Rule.from_text(rule_text)
                if rule is not None:
                    rules.append(rule)
                else:
                    final_result = rule_text
            assert final_result != ''
            workflows[name] = Workflow(rules, final_result)

        to_process = [(XmasRange(
            Range.closed(1, 4000), Range.closed(1, 4000),
            Range.closed(1, 4000), Range.closed(1, 4000)), 'in')]

        accepted_rating_numbers = 0
        while len(to_process) > 0:
            ranges, workflow_name = to_process.pop()
            if workflow_name == 'A':
                accepted_rating_numbers += ranges.possible_combinations()
                continue
            if workflow_name == 'R':
                continue
            workflow = workflows[workflow_name]
            to_process.extend(workflow.apply(ranges))

        log(RESULT, f'The total accepted rating numbers: {accepted_rating_numbers}')
        return accepted_rating_numbers


part = Part2()

part.add_result(167409079868000, """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
""")

part.add_result(131550418841958)
