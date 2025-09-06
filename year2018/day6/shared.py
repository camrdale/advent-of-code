from typing import Any

from aoc.map import Coordinate


class Destination:
    def __init__(self, text: str) -> None:
        self.location = Coordinate.from_text(text)
        self.infinite: bool | None = None
        self.closest_area: set[Coordinate] = set()

    def manhattan_distance(self, coordinate: Coordinate) -> int:
        return self.location.difference(coordinate).manhattan_distance()

    def __lt__(self, other: Any) -> bool:
        if type(other) != Destination:
            raise ValueError(f'Unexpected {other}')
        return self.location < other.location
