import math
from typing import NamedTuple, Self

from aoc import log
from aoc.range import Range


class ProductIdRange(NamedTuple):
    range: Range
    digits: int

    @classmethod
    def from_input(cls, input: str) -> list[Self]:
        result: list[Self] = []

        for range_input in input.split(','):
            full_range = Range.from_text(range_input)
            start_digits = math.floor(math.log10(full_range.start)) + 1
            end_digits = math.floor(math.log10(full_range.end)) + 1

            for digits in range(start_digits, end_digits + 1):
                assert full_range is not None, range_input
                lower_range, upper_range = full_range.split(10**digits)
                assert lower_range is not None, full_range
                result.append(cls(lower_range, digits))
                full_range = upper_range

            if full_range is not None:
                result.append(cls(full_range, end_digits))

        return result

    def sum_invalid(self, all_sequence_lengths: bool = False) -> int:
        invalid_ids: set[int] = set()
        sequence_range = [self.digits // 2] if self.digits % 2 == 0 else []
        if all_sequence_lengths:
            sequence_range = range(self.digits // 2, 0, -1)
        for sequence_length in sequence_range:
            if self.digits % sequence_length != 0:
                continue
            prefix_start = self.range.start // (10**(self.digits - sequence_length))
            prefix_end = self.range.end // (10**(self.digits - sequence_length))
            for prefix in range(prefix_start, prefix_end + 1):
                id = prefix
                for _ in range(self.digits // sequence_length - 1):
                    id = id * 10**sequence_length + prefix
                if self.range.contains_value(id):
                    invalid_ids.add(id)
                    log.log(log.INFO, f'Range {self} contains invalid ID: {id}')
        return sum(invalid_ids)
