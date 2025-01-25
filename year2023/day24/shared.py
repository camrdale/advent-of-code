from typing import NamedTuple, Any

from aoc import log
import aoc.map


class BigQuotient(NamedTuple):
    dividend: int
    divisor: int

    @classmethod
    def for_int(cls, other: int) -> 'BigQuotient':
        return BigQuotient(other, 1)

    def __add__(self, other: Any) -> 'BigQuotient':
        if type(other) == int:
            other = BigQuotient.for_int(other)
        if type(other) != BigQuotient:
            raise ValueError(f'{other} is not an int or BigQuotient')
        return BigQuotient((self.dividend*other.divisor) + (other.dividend*self.divisor), self.divisor*other.divisor)

    def __sub__(self, other: Any) -> 'BigQuotient':
        if type(other) == int:
            other = BigQuotient.for_int(other)
        if type(other) != BigQuotient:
            raise ValueError(f'{other} is not an int or BigQuotient')
        return BigQuotient((self.dividend*other.divisor) - (other.dividend*self.divisor), self.divisor*other.divisor)

    def __mul__(self, other: Any) -> 'BigQuotient':
        if type(other) == int:
            other = BigQuotient.for_int(other)
        if type(other) != BigQuotient:
            raise ValueError(f'{other} is not an int or BigQuotient')
        return BigQuotient(self.dividend*other.dividend, self.divisor*other.divisor)
    
    def __truediv__(self, other: Any) -> 'BigQuotient':
        if type(other) == int:
            other = BigQuotient.for_int(other)
        if type(other) != BigQuotient:
            raise ValueError(f'{other} is not an int or BigQuotient')
        return BigQuotient(self.dividend*other.divisor, self.divisor*other.dividend)

    def __eq__(self, other: Any) -> bool:
        if type(other) == int:
            other = BigQuotient.for_int(other)
        if type(other) != BigQuotient:
            return False
        return (self.dividend*other.divisor) == (other.dividend*self.divisor)

    def __le__(self, other: Any) -> bool:
        if type(other) == int:
            other = BigQuotient.for_int(other)
        if type(other) != BigQuotient:
            return False
        if self == other:
            return True
        if self.divisor*other.divisor < 0:
            return (self.dividend*other.divisor) > (other.dividend*self.divisor)
        return (self.dividend*other.divisor) < (other.dividend*self.divisor)
    
    def __ge__(self, other: Any) -> bool:
        if type(other) == int:
            other = BigQuotient.for_int(other)
        if type(other) != BigQuotient:
            return False
        if self == other:
            return True
        if self.divisor*other.divisor < 0:
            return (self.dividend*other.divisor) < (other.dividend*self.divisor)
        return (self.dividend*other.divisor) > (other.dividend*self.divisor)
    
    def __str__(self) -> str:
        return f'{self.dividend / self.divisor:.3f}'


class Hailstone(NamedTuple):
    position: aoc.map.Coordinate3D
    velocity: aoc.map.Offset3D

    @classmethod
    def from_text(cls, text: str) -> 'Hailstone':
        position_input, velocity_input = text.split('@')
        return cls(aoc.map.Coordinate3D.from_text(position_input), aoc.map.Offset3D.from_text(velocity_input))
    
    def m(self) -> BigQuotient:
        return BigQuotient(self.velocity.offset.y, self.velocity.offset.x)
    
    def b(self) -> BigQuotient:
        return BigQuotient.for_int(self.position.location.y) - (self.m() * self.position.location.x)

    def intersect(self, other: 'Hailstone', range_min: int, range_max: int) -> bool:
        m1 = self.m()
        m2 = other.m()
        b1 = self.b()
        b2 = other.b()

        if m1 == m2:
            if b1 == b2:
                return True
            else:
                log.log(log.INFO, f'Hailsone A: {self}')
                log.log(log.INFO, f'Hailsone B: {other}')
                log.log(log.INFO, f'Hailstones\' paths are parallel; they never intersect.\n')
                return False

        x = (b2 - b1) / (m1 - m2)
        y = (m1 * x) + b1

        if (not (x >= range_min)) or (not (x <= range_max)) or (not (y >= range_min)) or (not (y <= range_max)):
            log.log(log.INFO, f'Hailsone A: {self}')
            log.log(log.INFO, f'Hailsone B: {other}')
            log.log(log.INFO, f'Hailstones\' paths will cross outside the test area (at x={x}, y={y}).\n')
            return False

        if ((x >= self.position.location.x) and (self.velocity.offset.x < 0)) or (
            (x <= self.position.location.x) and (self.velocity.offset.x > 0)):
            log.log(log.INFO, f'Hailsone A: {self}')
            log.log(log.INFO, f'Hailsone B: {other}')
            log.log(log.INFO, f'Hailstones\' paths crossed in the past for hailstone A.\n')
            return False
        if ((x >= other.position.location.x) and (other.velocity.offset.x < 0)) or (
            (x <= other.position.location.x) and (other.velocity.offset.x > 0)):
            log.log(log.INFO, f'Hailsone A: {self}')
            log.log(log.INFO, f'Hailsone B: {other}')
            log.log(log.INFO, f'Hailstones\' paths crossed in the past for hailstone B.\n')
            return False
        
        log.log(log.INFO, f'Hailsone A: {self}')
        log.log(log.INFO, f'Hailsone B: {other}')
        log.log(log.INFO, f'Hailstones\' paths will cross inside the test area (at x={x}, y={y}).\n')
        return True

    def __str__(self) -> str:
        return f'{self.position.location.x}, {self.position.location.y}, {self.position.z} @ {self.velocity.offset.x}, {self.velocity.offset.y}, {self.velocity.z}'
