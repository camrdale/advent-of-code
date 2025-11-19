class Rule:
    def __init__(self, input: str) -> None:
        self.num = int(input.split(': ')[0])
        self.rule = input.split(': ')[1]

    def regex(self, rules: dict[int, Rule]) -> str:
        if '"' in self.rule:
            return self.rule.strip('"')

        if '|' not in self.rule:
            return self.regex_and(self.rule, rules)
        
        left, right = self.rule.split(' | ')
        return '(?:' + self.regex_and(left, rules) + '|' + self.regex_and(right, rules) + ')'

    def regex_and(self, rule: str, rules: dict[int, Rule]) -> str:
        result = ''
        for rule_id in rule.split(' '):
            result += rules[int(rule_id)].regex(rules)
        return result
