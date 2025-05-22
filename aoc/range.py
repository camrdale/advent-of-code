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
    
    def offset(self, delta: int) -> 'Range':
        """Return a new range offset from this one by delta."""
        return Range(self.start + delta, self.end + delta, self.closed_end)

    def split(self, value: int) -> 'tuple[Range|None, Range|None]':
        """Split this range at value, returning up to two new Ranges. The second range will start at value."""
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

    def __repr__(self) -> str:
        return f'[{self.start},{self.end}{"]" if self.closed_end else ")"}'
