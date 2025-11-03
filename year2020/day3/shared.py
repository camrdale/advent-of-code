from aoc.map import ParsedMap, Coordinate, Offset


TREE = '#'


class TobogganMap(ParsedMap):
    def __init__(self, lines: list[str]):
        super().__init__(lines, TREE)
    
    def path(self, slope: Offset) -> list[Coordinate]:
        trees: list[Coordinate] = []
        location = Coordinate(0, 0)
        while location.y <= self.max_y:
            if location in self.features[TREE]:
                trees.append(location)
            location = location.add(slope)
            if location.x > self.max_x:
                location = location._replace(x=location.x % (self.max_x + 1))
        return trees
