#!/usr/bin/python

from pathlib import Path
from collections import defaultdict

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'
TEST_RULES = """47|53
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
53|13"""
TEST_UPDATES = """75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

before_rules: dict[int, set[int]] = defaultdict(set)
manual_updates: list[list[int]] = []

with INPUT_FILE.open() as ifp:
    # for line in TEST_RULES.split('\n'):
    while line := ifp.readline():
        text = line.strip()
        if text == '':
            break
        # print('Parsing:', line)
        before, after = text.split('|')
        before_rules[int(after)].add(int(before))
    # for line in TEST_UPDATES.split('\n'):
    while line := ifp.readline():
        manual_updates.append(list(map(int, line.strip().split(','))))

# print(before_rules)
# print(manual_updates)

incorrect_updates: list[list[int]] = []
for update in manual_updates:
    # print('Checking update:', update)
    remaining_numbers = set(update)
    for page_number in update:
        remaining_numbers.remove(page_number)
        broken_rules = remaining_numbers.intersection(before_rules[page_number])
        if len(broken_rules) > 0:
            # print('  Violation for', page_number, 'which must occur after', broken_rules)
            incorrect_updates.append(update)
            break

for update in incorrect_updates:
    # print('Fixing update:', update)
    remaining_numbers = set(update)
    i = 0
    while i < len(update):
        page_number = update[i]
        remaining_numbers.remove(page_number)
        broken_rules = remaining_numbers.intersection(before_rules[page_number])
        if len(broken_rules) > 0:
            # print('  Violation for', page_number, 'which must occur after', broken_rules)
            del update[i]
            update.append(page_number)
            remaining_numbers.add(page_number)
        else:
            i += 1
    # print('Fixed update:', update)

middle_page_number_sum = 0
for update in incorrect_updates:
    # print('Re-checking update:', update)
    remaining_numbers = set(update)
    for page_number in update:
        remaining_numbers.remove(page_number)
        broken_rules = remaining_numbers.intersection(before_rules[page_number])
        if len(broken_rules) > 0:
            # print('  Violation for', page_number, 'which must occur after', broken_rules)
            break
    else:
        # print('No rules broken, adding', update[len(update) // 2], 'for:', update)
        middle_page_number_sum += update[len(update) // 2]

print('Sum of middle page numbers for corrected updates:', middle_page_number_sum)
