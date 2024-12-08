from typing import NamedTuple


class Offset(NamedTuple):
    x: int
    y: int

    def negate(self) -> 'Offset':
        return Offset(-self.x, -self.y)


class Node(NamedTuple):
    x: int
    y: int

    def difference(self, other: 'Node') -> Offset:
        return Offset(self.x - other.x, self.y - other.y)
    
    def add(self, offset: Offset) -> 'Node':
        return Node(self.x + offset.x, self.y + offset.y)
    
    def valid(self, width: int, height: int) -> bool:
        return 0 <= self.x < width and 0 <= self.y < height
