from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day7.shared import BagTreeNode


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        bags = BagTreeNode.parse_input(input)

        contains_bags = bags['shiny gold'].contains()

        log.log(log.RESULT, f'The number of bags required inside a shiny gold bag: {contains_bags}')
        return contains_bags


part = Part2()

part.add_result(32, """
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

part.add_result(126, """
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
""")

part.add_result(34862)
