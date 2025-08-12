class DisjointSetNode:
    """A node in a parent pointer tree structure."""

    def __init__(self) -> None:
        self.parent: DisjointSetNode = self
        self.size = 1


class DisjointSet:
    """Representation of a disjoint set as a forest of parent pointer trees."""

    def __init__(self, input: list[str]) -> None:
        self.nodes = [DisjointSetNode() for _ in range(len(input))]
        for line in input:
            left, right = line.split(' <-> ')
            node = int(left)
            for connected_node in right.split(', '):
                self.union(node, int(connected_node))

    def find(self, node_num: int) -> DisjointSetNode:
        node = self.nodes[node_num]

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

    def union(self, node_a: int, node_b: int) -> None:
        # Find the root of the trees for each node.
        root_node_a = self.find(node_a)
        root_node_b = self.find(node_b)
        if root_node_a == root_node_b:
            # They have the same root so are already unioned.
            return

        # Always merge the smaller set into the larger one.
        if root_node_a.size < root_node_b.size:
            root_node_a, root_node_b = root_node_b, root_node_a

        root_node_b.parent = root_node_a
        root_node_a.size += root_node_b.size
