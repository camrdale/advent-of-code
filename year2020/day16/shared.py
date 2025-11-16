import re

from aoc.range import Range


FIELD = re.compile('(.*): ([0-9]*)-([0-9]*) or ([0-9]*)-([0-9]*)')


class Field:
    def __init__(self, input: str) -> None:
        field = FIELD.fullmatch(input)
        assert field is not None, input
        self.name = field.group(1)
        self.lower_range = Range.closed(int(field.group(2)), int(field.group(3)))
        self.upper_range = Range.closed(int(field.group(4)), int(field.group(5)))

    def valid(self, value: int) -> bool:
        return self.lower_range.contains_value(value) or self.upper_range.contains_value(value)

    @classmethod
    def valid_for_any(cls, value: int, fields: list[Field]) -> bool:
        for field in fields:
            if field.valid(value):
                return True
        return False
