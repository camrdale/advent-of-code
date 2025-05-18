from abc import ABC, abstractmethod
import re

from aoc import log


class SnailfishNode(ABC):
    def __init__(self) -> None:
        self.parent: 'SnailfishBranch | None' = None

    @abstractmethod
    def magnitude(self) -> int:
        pass

    @abstractmethod
    def explode(self, depth_remaining: int = 4) -> bool:
        pass

    @abstractmethod
    def split(self) -> bool:
        pass

    def set_parent(self, parent: 'SnailfishBranch'):
        self.parent = parent


class SnailfishLeaf(SnailfishNode):
    def __init__(self, magnitude: int) -> None:
        super().__init__()
        self._magnitude = magnitude
    
    def magnitude(self) -> int:
        return self._magnitude
    
    def split(self) -> bool:
        if self._magnitude > 9:
            branch = SnailfishBranch(SnailfishLeaf(self._magnitude // 2), SnailfishLeaf(self._magnitude - (self._magnitude // 2)))
            assert self.parent is not None
            self.parent.replace_child(self, branch)
            return True
        return False
    
    def explode(self, depth_remaining: int = 4) -> bool:
        return False
    
    def add_magnitude(self, magnitude: int):
        self._magnitude += magnitude

    def __repr__(self) -> str:
        return f'{self._magnitude}'


class SnailfishBranch(SnailfishNode):
    def __init__(self, left: SnailfishNode, right: SnailfishNode) -> None:
        super().__init__()
        self.left: SnailfishNode = left
        self.right: SnailfishNode = right
        self.left.set_parent(self)
        self.right.set_parent(self)
    
    def magnitude(self) -> int:
        return self.left.magnitude() * 3 + self.right.magnitude() * 2
    
    def replace_child(self, old_child: SnailfishNode, new_child: SnailfishNode):
        if old_child is self.left:
            self.left = new_child
        elif old_child is self.right:
            self.right = new_child
        else:
            raise ValueError(f'No child found to replace: {old_child}')
        new_child.set_parent(self)

    def split(self) -> bool:
        if self.left.split():
            return True
        elif self.right.split():
            return True
        return False

    def explode(self, depth_remaining: int = 4) -> bool:
        if depth_remaining == 0:
            assert self.parent is not None
            assert isinstance(self.left, SnailfishLeaf)
            assert isinstance(self.right, SnailfishLeaf)
            left_leaf = self.left_leaf()
            if left_leaf is not None:
                left_leaf.add_magnitude(self.left.magnitude())
            right_leaf = self.right_leaf()
            if right_leaf is not None:
                right_leaf.add_magnitude(self.right.magnitude())
            leaf = SnailfishLeaf(0)
            self.parent.replace_child(self, leaf)
            return True
        
        if self.left.explode(depth_remaining=depth_remaining - 1):
            return True
        if self.right.explode(depth_remaining=depth_remaining - 1):
            return True
        return False
    
    def left_leaf(self) -> SnailfishLeaf | None:
        current = self
        # Walk up the tree until the current node is the right side
        while current.parent is not None and current.parent.left is current:
            current = current.parent
        if current.parent is None:
            return None
        
        # Walk down the right side of the node to the left
        current = current.parent.left
        while isinstance(current, SnailfishBranch):
            current = current.right
        assert isinstance(current, SnailfishLeaf)
        return current

    def right_leaf(self) -> SnailfishLeaf | None:
        current = self
        # Walk up the tree until the current node is the left side
        while current.parent is not None and current.parent.right is current:
            current = current.parent
        if current.parent is None:
            return None

        # Walk down the left side of the node to the right
        current = current.parent.right
        while isinstance(current, SnailfishBranch):
            current = current.left
        assert isinstance(current, SnailfishLeaf)
        return current

    def __repr__(self) -> str:
        return f'[{self.left},{self.right}]'


def parse_text(text: str) -> tuple[SnailfishNode, int]:
    if '0' <= text[0] <= '9':
        value = re.split(r'[,\]]', text)[0]
        return SnailfishLeaf(int(value)), len(value)

    assert text[0] == '['
    left, left_length = parse_text(text[1:])
    length = left_length + 1
    assert text[length] == ','
    right, right_length = parse_text(text[length+1:])
    length += right_length + 1
    assert text[length] == ']'
    branch = SnailfishBranch(left, right)
    return branch, length + 1


def reduce(snailfish: SnailfishNode):
    while True:
        if snailfish.explode():
            log.log(log.DEBUG, f'Exploded: {snailfish}')
            continue
        if not snailfish.split():
            return
        log.log(log.DEBUG, f'Split: {snailfish}')
