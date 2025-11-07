from dataclasses import dataclass, field
import re


BAG = re.compile(r'([a-z ]*) bags contain (.*)\.')
CONTAINS = re.compile(r'([0-9]*) ([a-z ]*) bags?')


@dataclass(unsafe_hash=True)
class BagTreeNode:
    color: str
    parents: list[BagTreeNode] = field(default_factory=lambda: [], hash=False, compare=False)
    children: dict[BagTreeNode, int] = field(default_factory=lambda: {}, hash=False, compare=False)

    @classmethod
    def parse_input(cls, input:list[str]) -> dict[str, BagTreeNode]:
        bags: dict[str, BagTreeNode] = {}
        for line in input:
            match = BAG.fullmatch(line)
            assert match is not None, line

            parent = match.group(1)
            if parent not in bags:
                bags[parent] = BagTreeNode(parent)

            if match.group(2) == 'no other bags':
                continue
            for contains_input in match.group(2).split(', '):
                contains = CONTAINS.fullmatch(contains_input)
                assert contains is not None, contains_input

                color = contains.group(2)
                if color not in bags:
                    bags[color] = BagTreeNode(color)

                bags[color].parents.append(bags[parent])
                bags[parent].children[bags[color]] = int(contains.group(1))

        return bags

    def can_contain(self) -> set[str]:
        result: set[str] = set()
        for bag in self.parents:
            result.add(bag.color)
            result.update(bag.can_contain())
        return result

    def contains(self) -> int:
        result = 0
        for bag, count in self.children.items():
            result += count + count * bag.contains()
        return result
