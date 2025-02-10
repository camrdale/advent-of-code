import math
from typing import NamedTuple, Self, Any

import aoc.map


class NormalizedDirection(NamedTuple):
    """A direction normalized so that one of the x/y have magnitude of 1 and the other's magnitude is between 0 and 1."""
    x: float
    y: float

    @classmethod
    def from_offset(cls, offset: aoc.map.Offset) -> Self:
        normalize_by = max(abs(offset.x), abs(offset.y))
        return cls(offset.x / normalize_by, offset.y / normalize_by)

    def negate(self) -> 'NormalizedDirection':
        return NormalizedDirection(-self.x, -self.y)
    
    def angle(self) -> float:
        """Returns the angle (in degrees) of the direction from UP (0,-1), in the range 0 to 360."""
        return (math.degrees(math.atan2(self.y, self.x)) + 90.0) % 360.0
    
    def __lt__(self, other: Any) -> bool:
        """Default sort for directions is by angle from UP."""
        if type(other) != NormalizedDirection:
            raise ValueError(f'Unexpected {other}')
        return self.angle() < other.angle()
