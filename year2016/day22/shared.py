import re
from typing import Self

from aoc.map import Coordinate


NODE = re.compile(
    r'/dev/grid/node-x([0-9]*)-y([0-9]*)[ ]*([0-9]*)T[ ]*([0-9]*)T[ ]*([0-9]*)T[ ]*([0-9]*)%')


class Node:
    def __init__(self, location: Coordinate, size: int, used: int, available: int) -> None:
        self.location = location
        self.size = size
        self.used = used
        self.available = available
    
    @classmethod
    def from_text(cls, text: str) -> Self:
        node = NODE.match(text)
        assert node is not None, text
        return cls(
            Coordinate(int(node.group(1)), int(node.group(2))),
            int(node.group(3)),
            int(node.group(4)),
            int(node.group(5)))
