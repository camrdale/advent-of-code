from aoc.map import UnknownMap, Coordinate


WALL = '#'
OPEN = ' '


class OfficeMaze(UnknownMap):
    def __init__(self, designers_number: int):
        super().__init__(WALL + OPEN)
        self.designers_number = designers_number
        
    def valid(self, coordinate: Coordinate) -> bool:
        if coordinate.x < 0 or coordinate.y < 0:
            return False
        if coordinate in self.features[WALL]:
            return False
        if coordinate in self.features[OPEN]:
            return True
        value = coordinate.x*coordinate.x + 3*coordinate.x + 2*coordinate.x*coordinate.y + coordinate.y + coordinate.y*coordinate.y
        value += self.designers_number
        if value.bit_count() % 2 == 0:
            self.add_feature(OPEN, coordinate)
            return True
        self.add_feature(WALL, coordinate)
        return False
