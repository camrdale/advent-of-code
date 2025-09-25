from collections.abc import Hashable
from typing import TypeVar


class DisjointSetNode:
    """A node in a parent pointer tree structure."""

    def __init__(self) -> None:
        self.parent: DisjointSetNode = self
        # The size is only accurate for nodes that are the root of a tree.
        self.size = 1


T = TypeVar('T', bound=Hashable)


class DisjointSet[T]:
    """Representation of a disjoint set as a forest of parent pointer trees."""

    def __init__(self) -> None:
        self.nodes: dict[T, DisjointSetNode] = {}

    def add(self, node_id: T) -> None:
        """Add a node identified by node_id to the forest as a new 1-element set."""
        if node_id not in self.nodes:
            self.nodes[node_id] = DisjointSetNode()

    def find(self, node_id: T) -> DisjointSetNode:
        """Find the root of the set that contains the node identified by node_id."""
        node = self.nodes[node_id]

        # Find the root of the tree for this node.
        root = node
        while root.parent != root:
            root = root.parent

        # Update the parents along the path so future finds are faster.
        while node.parent != root:
            old_parent = node.parent
            node.parent = root
            node = old_parent

        return root

    def union(self, node_a_id: T, node_b_id: T) -> None:
        """Merge the sets identified by two node ids."""
        # Find the root of the trees for each node.
        root_node_a = self.find(node_a_id)
        root_node_b = self.find(node_b_id)
        if root_node_a == root_node_b:
            # They have the same root so are already unioned.
            return

        # Always merge the smaller set into the larger one.
        if root_node_a.size < root_node_b.size:
            root_node_a, root_node_b = root_node_b, root_node_a

        root_node_b.parent = root_node_a
        root_node_a.size += root_node_b.size

    def size(self) -> int:
        """Returns the number of disjoint sets."""
        return sum(node.parent == node for node in self.nodes.values())
