import string
from typing import NamedTuple
from types import NotImplementedType

from aoc.log import log, DEBUG, INFO
from aoc.map import Offset, Coordinate, ParsedMap


DOWNSTREAM_NEIGHBORS = [
    Offset(1, 0),
    Offset(0, 1)]


class Fence(NamedTuple):
    """A fence between two neighboring plots."""
    topleft: Coordinate
    bottomright: Coordinate

    @classmethod
    def deterministic(cls, coord1: Coordinate, coord2: Coordinate) -> 'Fence':
        """Create a Fence with a deterministic ordering of the neighboring plots."""
        l = sorted([coord1, coord2])
        return cls(l[0], l[1])
    
    def neighbor(self, other: 'Fence') -> bool:
        """Determine if the other fence neighbors this one."""
        if self.topleft.y == self.bottomright.y:
            # Vertical fence
            if other.topleft.y != other.bottomright.y:
                # Other must also be vertical
                return False
            if other.topleft.x != self.topleft.x or other.bottomright.x != other.bottomright.x:
                # Other must be in the same column
                return False
            if abs(other.topleft.y - self.topleft.y) == 1:
                # Other must be neighboring vertically
                return True
        else:
            # Horizontal fence
            if other.topleft.x != other.bottomright.x:
                # Other must also be horizontal
                return False
            if other.topleft.y != self.topleft.y or other.bottomright.y != other.bottomright.y:
                # Other must be in the same row
                return False
            if abs(other.topleft.x - self.topleft.x) == 1:
                # Other must be neighboring horizontally
                return True
        return False


class Side:
    """A collection of fences that form a continuous side of a region."""

    def __init__(self, fence: Fence, inside: bool):
        """Create a new Side with an initial fence, containing plots inside or outside the fence."""
        self.initial_fence = fence
        self.fences: set[Fence] = set([fence])
        self.inside = inside
    
    def __hash__(self) -> int:
        return hash((self.initial_fence, self.inside))
    
    def __eq__(self, other: object) -> bool | NotImplementedType:
        if not isinstance(other, Side):
            return NotImplemented
        return self.initial_fence == other.initial_fence and self.inside == other.inside
    
    def __str__(self) -> str:
        return ('Side(' + str(self.initial_fence) + ', ' + str(self.inside) + ', ' + str(self.fences))


class Region:
    def __init__(self, plant: str, location: Coordinate):
        """Create an initial region containing a single plot."""
        self.plant = plant
        self.initial_location = location
        self.locations: set[Coordinate] = set([location])
        self.fences: set[Fence] = set()
        for neighbor in location.neighbors():
            self.fences.add(Fence.deterministic(location, neighbor))

    def merge(self, other: 'Region'):
        """Merge another region into this one."""
        log(DEBUG, 'Merging', other.initial_location, 'into', self.initial_location)
        assert(other.initial_location != self.initial_location)
        assert(other.plant == self.plant)
        self.locations.update(other.locations)
        self.fences = self.fences ^ other.fences
    
    def price(self) -> int:
        """Calculate the price of this region."""
        log(INFO, 'A region of', self.plant, 'plants with price',
            len(self.locations), '*', len(self.fences), '=', len(self.locations) * len(self.fences))
        return len(self.locations) * len(self.fences)
    
    def discounted_price(self) -> int:
        """Calculate the discounted price of this region."""
        sides: list[Side] = []
        for fence in sorted(self.fences):
            inside = fence.topleft in self.locations
            merged = False
            for side in sides:
                if side.inside != inside:
                    continue
                for other_fence in side.fences:
                    if fence.neighbor(other_fence):
                        side.fences.add(fence)
                        merged = True
                        break
                if merged:
                    break
            if not merged:
                sides.append(Side(fence, inside))
        log(INFO, 'A region of', self.plant, 'plants with discounted price',
            len(self.locations), '*', len(sides), '=', len(self.locations) * len(sides))
        return len(self.locations) * len(sides)
    
    def __hash__(self) -> int:
        return hash(self.initial_location)
    
    def __eq__(self, other: object) -> bool | NotImplementedType:
        if not isinstance(other, Region):
            return NotImplemented
        return self.initial_location == other.initial_location
    
    def __str__(self) -> str:
        return ('Region(' + self.plant + ', ' + str(self.initial_location) + ', '
                + str(self.locations) + ', ' + str(self.fences))


class Garden(ParsedMap):
    def __init__(self, lines: list[str]):
        super().__init__(lines, string.ascii_uppercase)
        self.regions: dict[Coordinate, Region] = {}
        for c, coordinates in self.features.items():
            for coordinate in coordinates:
                self.regions[coordinate] = Region(c, coordinate)

    def merge(self):
        """Merge any neighboring plots of the same type."""
        for y in range(self.height):
            for x in range(self.width):
                c = Coordinate(x,y)
                log(DEBUG, 'Processing', c)
                region = self.regions[c]
                for neighbor_offset in DOWNSTREAM_NEIGHBORS:
                    neighbor = c.add(neighbor_offset)
                    if neighbor.valid(self.width, self.height):
                        log(DEBUG, 'Checking', region.plant, 'at', c, 'against', neighbor)
                        neighbor_region = self.regions[neighbor]
                        if neighbor_region.plant == region.plant and neighbor_region != region:
                            region.merge(neighbor_region)
                            for location in neighbor_region.locations:
                                log(DEBUG, 'Pointing dict for', location, 'from region', self.regions[location], 'to merged region', region)
                                self.regions[location] = region

    def price(self) -> int:
        """Calculate the price of all the regions."""
        return sum(region.price() for region in set(self.regions.values()))

    def discounted_price(self) -> int:
        """Calculate the price of all the regions."""
        return sum(region.discounted_price() for region in set(self.regions.values()))
    
    def __str__(self) -> str:
        s = ''
        for y in range(self.height):
            for x in range(self.width):
                c = Coordinate(x,y)
                region = self.regions[c]
                s += region.plant
            s += '\n'
        s += '\n'
        for region in set(self.regions.values()):
            s += str(region) + '\n'
        return s
