import bisect
from collections.abc import Iterator, Iterable
import operator
from typing import NamedTuple, Self


class Range(NamedTuple):
    """Represents a range of values. Ranges are always closed on the start but can be open at (not include) the end."""
    start: int
    end: int
    closed_end: bool

    @classmethod
    def open(cls, start: int, end: int) -> Self:
        """Creates a new open-ended Range."""
        return cls(start, end, False)

    @classmethod
    def closed(cls, start: int, end: int) -> Self:
        """Creates a new closed-ended Range."""
        return cls(start, end, True)
    
    @classmethod
    def from_text(cls, text: str, closed: bool = True) -> Self:
        """Creates a new (closed-ended by default) Range from text of the form '123-456'."""
        start, end = text.split('-')
        return cls(int(start), int(end), closed)

    def length(self) -> int:
        return self.end - self.start + (1 if self.closed_end else 0)
    
    def intersects(self, other: 'Range') -> bool:
        """Returns true if this Range overlaps with the other."""
        if not self.closed_end and other.start >= self.end:
            return False
        if not other.closed_end and self.start >= other.end:
            return False
        if self.closed_end and other.start > self.end:
            return False
        if other.closed_end and self.start > other.end:
            return False
        return True
    
    def contains(self, other: 'Range') -> bool:
        """Returns true if this Range contains the other."""
        if self.start > other.start:
            return False
        if self.end - (1 if not self.closed_end else 0) < other.end - (1 if not other.closed_end else 0):
            return False
        return True
    
    def contains_value(self, value: int) -> bool:
        """Returns true if this Range contains the value."""
        if self.start > value:
            return False
        if self.end - (1 if not self.closed_end else 0) < value:
            return False
        return True
    
    def offset(self, delta: int) -> 'Range':
        """Return a new range offset from this one by delta."""
        return Range(self.start + delta, self.end + delta, self.closed_end)

    def split(self, value: int | None = None) -> 'tuple[Range|None, Range|None]':
        """Split this range, returning up to two new Ranges.
        
        The split will be at value, such that the second range will start at value.
        If value is not specified, the split will be in the middle of the range.
        """
        if value is None:
            value = (self.start + self.end) // 2 + 1
        lower_range = None
        upper_range = None
        if value > self.start:
            lower_range = Range(self.start, min(value - 1, self.end), self.closed_end)
        if value <= self.end:
            upper_range = Range(max(self.start, value), self.end, self.closed_end)
        return lower_range, upper_range
    
    def merge(self, other: 'Range') -> 'Range | None':
        """Merge this Range with the other, returns None if they don't intersect."""
        if not self.intersects(other):
            return None
        start = min(self.start, other.start)
        end = max(self.end, other.end)
        closed_end = other.closed_end
        if end == self.end and end != other.end:
            closed_end = self.closed_end
        if other.end == self.end:
            closed_end = max(self.closed_end, other.closed_end)
        return Range(start, end, closed_end)

    def closest_to(self, value: int) -> int:
        """Return the closest to the value that is in the range."""
        if value < self.start:
            return self.start
        elif value >= self.end:
            return self.end - (1 if not self.closed_end else 0)
        return value

    def __repr__(self) -> str:
        return f'[{self.start},{self.end}{"]" if self.closed_end else ")"}'


class Ranges(Iterable[Range]):
    """A list of Ranges, maintained such that overlapping Ranges are merged."""

    def __init__(self) -> None:
        # Sorted list (by start of the range) of non-overlapping Range objects.
        self.ranges: list[Range] = []

    def add(self, range: Range):
        """Add a Range to the list, merging it with any Ranges it overlaps with."""
        i = bisect.bisect_left(self.ranges, range.start, key=operator.attrgetter('start'))
        if i > 0 and self.ranges[i-1].intersects(range):
            i -= 1
        while i < len(self.ranges) and (merged := self.ranges[i].merge(range)) is not None:
            range = merged
            del self.ranges[i]
        self.ranges.insert(i, range)

    def __iter__(self) -> Iterator[Range]:
        for range in self.ranges:
            yield range

    def __repr__(self) -> str:
        return str(self.ranges)
