import math
import re
from typing import Any

from aoc.map import Coordinate, Coordinate3D, Offset3D


PARTICLE = re.compile(f'p=<([^>]*)>, v=<([^>]*)>, a=<([^>]*)>')

ORIGIN = Coordinate3D(0, Coordinate(0,0))


def safe_division(numerator: float, denominator: float) -> float:
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return 0.0


def zeroes(p: int, v: int, a: int) -> list[int]:
    t: list[int] = []

    # Position crosses 0 when p + v * t + a * t * (t+1) / 2 = 0
    if a == 0:
        # if a == 0:  t = - p / v
        t.append(math.ceil(safe_division(p, v)) + 1)
    else:
        # (a/2) * t^2 + (v + a/2) * t + p = 0
        # t = ( -v - a/2 +/- sqrt((v + a/2)^2 - 2 * p * a)) / a
        try:
            f = math.sqrt((v + a/2)**2 - 2 * p * a)
            t.append(math.ceil((-v - a/2 + f) / a) + 1)
            t.append(math.ceil((-v - a/2 - f) / a) + 1)
        except ValueError:
            pass

    return t


class Particle:
    def __init__(self, num: int, input: str) -> None:
        self.num = num
        match = PARTICLE.match(input)
        assert match is not None, input
        self.p = Coordinate3D.from_text(match.group(1))
        self.v = Offset3D.from_text(match.group(2))
        self.a = Offset3D.from_text(match.group(3))
        self.t = 0

    def advance(self, t: int) -> None:
        """Advance the particle t steps in time."""
        self.p = self.p.add(self.v.times(t)).add(self.a.times(t * (t+1) // 2))
        self.v = self.v.add(self.a.times(t))
        self.t += t
    
    def moving_outward(self) -> bool:
        """Check if the particle is forever moving outward from the origin.
        
        If the position, velocity and acceleration all have the same sign,
        along all 3 axes, it will always be moving away from the origin.
        """
        if self.p.z * self.v.z < 0 or self.p.location.x * self.v.offset.x < 0 or self.p.location.y * self.v.offset.y < 0:
            return False
        if self.p.z * self.a.z < 0 or self.p.location.x * self.a.offset.x < 0 or self.p.location.y * self.a.offset.y < 0:
            return False
        return True
    
    def when_moving_outward(self) -> int:
        """Determine how long until the particle is forever moving outward from the origin."""
        times = [0]

        # Velocity crosses 0 at t = - v / a
        times.append(math.ceil(safe_division(-self.v.z, self.a.z)) + 1)
        times.append(math.ceil(safe_division(-self.v.offset.x, self.a.offset.x)) + 1)
        times.append(math.ceil(safe_division(-self.v.offset.y, self.a.offset.y)) + 1)

        times.extend(zeroes(self.p.z, self.v.z, self.a.z))
        times.extend(zeroes(self.p.location.x, self.v.offset.x, self.a.offset.x))
        times.extend(zeroes(self.p.location.y, self.v.offset.y, self.a.offset.y))

        return max(times)
    
    def manhattan_distance(self) -> int:
        """Distance of the particle from the origin."""
        return self.p.difference(ORIGIN).manhattan_distance()

    def magnitude(self) -> tuple[int, int, int]:
        """Returns a relative magnitude of the acceleration/velocity/position of the particle, for sorting.
        
        Only useful to compare particles that are forever moving outward from the origin.
        """
        return self.a.manhattan_distance(), self.v.manhattan_distance(), self.manhattan_distance()

    def __lt__(self, other: Any) -> bool:
        if type(other) != Particle:
            raise ValueError(f'Unexpected {other}')
        return self.magnitude() < other.magnitude()
    
    def __eq__(self, other: Any) -> bool:
        if type(other) != Particle:
            return False
        return self.magnitude() == other.magnitude()

    def __repr__(self) -> str:
        return f'Particle({self.num}, p={self.p}, v={self.v}, a={self.a}, t={self.t})'
