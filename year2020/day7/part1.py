from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day7.shared import BagTreeNode


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        bags = BagTreeNode.parse_input(input)

        can_contain_bags = bags['shiny gold'].can_contain()

        log.log(log.RESULT, f'The number of bags that can eventually contain a shiny gold bag: {len(can_contain_bags)}')
        return len(can_contain_bags)


part = Part1()

part.add_result(4, """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""")

part.add_result(124)
