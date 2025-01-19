from collections.abc import Callable
import operator
import re
from typing import NamedTuple

from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
import aoc.runner

PART_PARSER = re.compile(r'{x=([0-9]*),m=([0-9]*),a=([0-9]*),s=([0-9]*)}')
RULE_PARSER = re.compile(r'([xmas])([<>])([0-9]*):(.*)')


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_text(cls, text: str) -> 'Part':
        match = PART_PARSER.match(text)
        if match is None:
            raise ValueError(f'Failed to parse Part from: {text}')
        return cls(int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4)))

    def get(self, rating: str) -> int:
        return getattr(self, rating)
    
    def rating_number(self) -> int:
        return self.x + self.m + self.a + self.s
    
    def __str__(self) -> str:
        return f'{{x={self.x},m={self.m},a={self.a},s={self.s}}}'


class Rule(NamedTuple):
    rating: str
    operator: Callable[[int, int], bool]
    value: int
    result: str

    @classmethod
    def from_text(cls, rule_text: str) -> 'Rule | None':
        match = RULE_PARSER.match(rule_text)
        if match is not None:
            op = operator.lt if match.group(2) == '<' else operator.gt
            return cls(match.group(1), op, int(match.group(3)), match.group(4))
        return None

    def apply(self, part: Part) -> str | None:
        if self.operator(part.get(self.rating), self.value):
            return self.result
        return None


class Workflow:
    def __init__(self, rules: list[Rule], final_result: str):
        self.rules: list[Rule] = rules
        self.final_result = final_result

    def apply(self, part: Part) -> str:
        for rule in self.rules:
            result = rule.apply(part)
            if result is not None:
                return result
        return self.final_result


class Part1(aoc.runner.Part):
    def run(self, parser: InputParser) -> int:
        workflow_input, part_input = parser.get_two_part_input()

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
            
        accepted_rating_numbers = 0
        for line in part_input:
            part = Part.from_text(line)
            next_workflow = 'in'
            workflow_chain = ''
            while next_workflow != 'A' and next_workflow != 'R':
                workflow_chain += next_workflow + ' -> '
                workflow = workflows[next_workflow]
                next_workflow = workflow.apply(part)
            if next_workflow == 'A':
                accepted_rating_numbers += part.rating_number()
            log(INFO, f'{part}: {workflow_chain}{next_workflow}')

        log(RESULT, f'The total accepted rating numbers: {accepted_rating_numbers}')
        return accepted_rating_numbers


part = Part1()

part.add_result(19114, """
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

part.add_result(480738)
