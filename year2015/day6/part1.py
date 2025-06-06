import re
from typing import NamedTuple

from aoc.input import InputParser
from aoc import log
from aoc.range import Range
from aoc.runner import Part


INSTRUCTION = re.compile(r'(turn on|toggle|turn off) ([0-9]*),([0-9]*) through ([0-9]*),([0-9]*)')


class Range2D(NamedTuple):
    x: Range
    y: Range

    def size(self) -> int:
        return self.x.length() * self.y.length()

    def intersects(self, other: 'Range2D') -> bool:
        return self.x.intersects(other.x) and self.y.intersects(other.y)
    
    def subtract(self, other: 'Range2D') -> list['Range2D']:
        """Returns the ranges resulting from subtracting other from this range."""
        if not self.intersects(other):
            return [self]
        result: list[Range2D] = []
        unsplit = self

        outside_x, upper_x = unsplit.x.split(other.x.start)
        if outside_x is not None:
            result.append(Range2D(outside_x, unsplit.y))
        if upper_x is None:
            return result
        unsplit_x, outside_x = upper_x.split(other.x.end + 1)
        if outside_x is not None:
            result.append(Range2D(outside_x, unsplit.y))
        if unsplit_x is None:
            return result
        unsplit = unsplit._replace(x=unsplit_x)

        outside_y, upper_y = unsplit.y.split(other.y.start)
        if outside_y is not None:
            result.append(Range2D(unsplit.x, outside_y))
        if upper_y is None:
            return result
        unsplit_y, outside_y = upper_y.split(other.y.end + 1)
        if outside_y is not None:
            result.append(Range2D(unsplit.x, outside_y))
        if unsplit_y is None:
            return result
        unsplit = unsplit._replace(y=unsplit_y)

        return result
    
    def subtract_from_all(self, others: list['Range2D']) -> list['Range2D']:
        """Subtract this range from all the ones in others."""
        result: list[Range2D] = []
        for range in others:
            result.extend(range.subtract(self))
        return result
    
    def subtract_all(self, others: list['Range2D']) -> list['Range2D']:
        """Subtract all the ranges in others from this range."""
        remaining: list[Range2D] = [self]
        for other in others:
            new_remaining: list[Range2D] = []
            for range in remaining:
                if not range.intersects(other):
                    new_remaining.append(range)
                else:
                    new_remaining.extend(range.subtract(other))
            remaining = new_remaining
        return remaining

    def __repr__(self) -> str:
        return f'{self.x}-{self.y}'
    

class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        lights: list[Range2D] = []
        for line in input:
            instruction = INSTRUCTION.match(line)
            if instruction is None:
                raise ValueError(f'Failed to parse: {line}')

            x1, y1, x2, y2 = map(int, instruction.groups()[1:])
            assert x2 >= x1
            assert y2 >= y1

            range = Range2D(Range.closed(x1, x2), Range.closed(y1, y2))
            
            new_lights = range.subtract_from_all(lights)
            match instruction.group(1):
                case 'turn on':
                    new_lights.append(range)
                case 'turn off':
                    pass
                case 'toggle':
                    new_lights.extend(range.subtract_all(lights))
                case _:
                    raise ValueError(f'Unexpected instruction "{instruction.group(1)}": {line}')

            lights = new_lights

        total_on = sum(range.size() for range in lights)
        log.log(log.RESULT, f'The number of lights turned on: {total_on}')
        return total_on


part = Part1()

part.add_result(1000000, """
turn on 0,0 through 999,999
""")

part.add_result(1000, """
toggle 0,0 through 999,0
""")

part.add_result(0, """
turn off 499,499 through 500,500
""")

part.add_result(1000000 - 1000 - 4, """
turn on 0,0 through 999,999
toggle 0,0 through 999,0
turn off 499,499 through 500,500
""")

part.add_result(569999)
