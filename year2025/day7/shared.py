from collections import defaultdict

from aoc.map import ParsedMap, DOWN, LEFT, RIGHT, Coordinate


START = 'S'
SPLITTER = '^'


class TachyonMap(ParsedMap):
    def __init__(self, lines: list[str]):
        super().__init__(lines, START + SPLITTER)
    
    def shoot_beam(self) -> tuple[int, int]:
        num_splits = 0
        num_timelines = 0

        start = next(iter(self.features[START]))
        active_beams: dict[Coordinate, int] = {start.add(DOWN): 1}

        while active_beams:
            next_beams: dict[Coordinate, int] = defaultdict(int)

            for beam, timelines in active_beams.items():
                next_beam = beam.add(DOWN)
                if not self.valid(next_beam):
                    num_timelines += timelines
                    continue
                if next_beam not in self.features[SPLITTER]:
                    next_beams[next_beam] += timelines
                    continue
                num_splits += 1
                next_beams[next_beam.add(LEFT)] += timelines
                next_beams[next_beam.add(RIGHT)] += timelines

            active_beams = next_beams

        return num_splits, num_timelines
