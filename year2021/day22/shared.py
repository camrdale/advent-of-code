import re
from typing import NamedTuple, Self

from aoc.range import Range


REBOOT_STEP = re.compile(r'(on|off) x=([0-9-]*)..([0-9-]*),y=([0-9-]*)..([0-9-]*),z=([0-9-]*)..([0-9-]*)')


class Cuboid(NamedTuple):
    x: Range
    y: Range
    z: Range

    @classmethod
    def from_text(cls, text: str, clamp: Range | None = None) -> tuple[Self | None, bool]:
        match = REBOOT_STEP.match(text)
        assert match is not None
        x = Range.closed(int(match.group(2)), int(match.group(3)))
        y = Range.closed(int(match.group(4)), int(match.group(5)))
        z = Range.closed(int(match.group(6)), int(match.group(7)))
        on = match.group(1) == 'on'

        if clamp is not None:
            if not clamp.contains(x):
                _, x = x.split(clamp.start)
                if x is None:
                    return None, on
                x, _ = x.split(clamp.end + 1)
                if x is None:
                    return None, on
            if not clamp.contains(y):
                _, y = y.split(clamp.start)
                if y is None:
                    return None, on
                y, _ = y.split(clamp.end + 1)
                if y is None:
                    return None, on
            if not clamp.contains(z):
                _, z = z.split(clamp.start)
                if z is None:
                    return None, on
                z, _ = z.split(clamp.end + 1)
                if z is None:
                    return None, on

        return cls(x, y, z), on
    
    def size(self) -> int:
        return self.x.length() * self.y.length() * self.z.length()

    def intersects(self, other: 'Cuboid') -> bool:
        return self.x.intersects(other.x) and self.y.intersects(other.y) and self.z.intersects(other.z)
    
    def subtract(self, other: 'Cuboid') -> list['Cuboid']:
        """Returns the cuboids resulting from subtracting other from this cuboid."""
        if not self.intersects(other):
            return [self]
        result: list[Cuboid] = []
        unsplit = self

        outside_x, upper_x = unsplit.x.split(other.x.start)
        if outside_x is not None:
            result.append(Cuboid(outside_x, unsplit.y, unsplit.z))
        if upper_x is None:
            return result
        unsplit_x, outside_x = upper_x.split(other.x.end + 1)
        if outside_x is not None:
            result.append(Cuboid(outside_x, unsplit.y, unsplit.z))
        if unsplit_x is None:
            return result
        unsplit = unsplit._replace(x=unsplit_x)

        outside_y, upper_y = unsplit.y.split(other.y.start)
        if outside_y is not None:
            result.append(Cuboid(unsplit.x, outside_y, unsplit.z))
        if upper_y is None:
            return result
        unsplit_y, outside_y = upper_y.split(other.y.end + 1)
        if outside_y is not None:
            result.append(Cuboid(unsplit.x, outside_y, unsplit.z))
        if unsplit_y is None:
            return result
        unsplit = unsplit._replace(y=unsplit_y)

        outside_z, upper_z = unsplit.z.split(other.z.start)
        if outside_z is not None:
            result.append(Cuboid(unsplit.x, unsplit.y, outside_z))
        if upper_z is None:
            return result
        unsplit_z, outside_z = upper_z.split(other.z.end + 1)
        if outside_z is not None:
            result.append(Cuboid(unsplit.x, unsplit.y, outside_z))
        if unsplit_z is None:
            return result
        unsplit = unsplit._replace(z=unsplit_z)

        return result
    
    def subtract_from_all(self, others: list['Cuboid']) -> list['Cuboid']:
        """Subtract this cuboid from all the ones in others."""
        result: list[Cuboid] = []
        for cuboid in others:
            result.extend(cuboid.subtract(self))
        return result
