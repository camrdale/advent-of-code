import re
from typing import NamedTuple, Self


REINDEER = re.compile(r'(.*) can fly ([0-9]*) km/s for ([0-9]*) seconds, but then must rest for ([0-9]*) seconds.')


class Reindeer(NamedTuple):
    name: str
    speed: int
    speed_time: int
    rest_time: int

    @classmethod
    def from_text(cls, text: str) -> Self:
        reindeer = REINDEER.match(text)
        assert reindeer is not None, text
        return cls(reindeer.group(1), int(reindeer.group(2)), int(reindeer.group(3)), int(reindeer.group(4)))

    def distance(self, time: int) -> int:
        """The total distance traveled by this reindeer in the given time."""
        full_cycles = time // (self.speed_time + self.rest_time)
        distance = full_cycles * self.speed * self.speed_time
        partial_cycle = time % (self.speed_time + self.rest_time)
        distance += self.speed * min(self.speed_time, partial_cycle)
        return distance
