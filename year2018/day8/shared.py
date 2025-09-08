from typing import Self


class Node:
    def __init__(self, children: list[Node], metadata: list[int]) -> None:
        self.children = children
        self.metadata = metadata

    @classmethod
    def parse(cls, license_file: list[int], start: int) -> tuple[Self, int]:
        """Parse a node from the license file, starting at index start.
        
        Returns the parsed node and the next index after the node.
        """
        num_children = license_file[start]
        num_metadata = license_file[start + 1]
        children: list[Node] = []
        index = start + 2
        for _ in range(num_children):
            child, index = cls.parse(license_file, index)
            children.append(child)
        return cls(children, license_file[index:index+num_metadata]), index + num_metadata

    def sum_metadata(self) -> int:
        return sum(self.metadata) + sum(child.sum_metadata() for child in self.children)

    def value(self) -> int:
        if not self.children:
            return sum(self.metadata)
        return sum(
            self.children[i - 1].value() if 0 < i <= len(self.children) else 0
            for i in self.metadata)
