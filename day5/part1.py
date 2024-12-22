from collections import defaultdict

from aoc.input import InputParser
from aoc.log import log, RESULT, INFO, DEBUG
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        rules_input, pages_input = parser.get_two_part_input()

        before_rules: dict[int, set[int]] = defaultdict(set)
        for line in rules_input:
            before, after = line.split('|')
            before_rules[int(after)].add(int(before))

        manual_updates: list[list[int]] = [list(map(int, line.split(','))) for line in pages_input]

        log(DEBUG, before_rules)
        log(DEBUG, manual_updates)

        middle_page_number_sum = 0
        for update in manual_updates:
            log(DEBUG, 'Checking update:', update)
            remaining_numbers = set(update)
            for page_number in update:
                remaining_numbers.remove(page_number)
                broken_rules = remaining_numbers.intersection(before_rules[page_number])
                if len(broken_rules) > 0:
                    log(INFO, '  Violation for', page_number, 'which must occur after', broken_rules)
                    break
            else:
                log(INFO, 'No rules broken, adding', update[len(update) // 2], 'for:', update)
                middle_page_number_sum += update[len(update) // 2]

        log(RESULT, 'Sum of middle page numbers of valid updates:', middle_page_number_sum)
        return middle_page_number_sum


part = Part1()

part.add_result(143, """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""")

part.add_result(5639)
