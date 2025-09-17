import re

from aoc import log
from aoc.map import UnknownMap, Coordinate, DOWN, LEFT, RIGHT, UP


CLAY = '#'
WATER = '~'
FLOW = '|'

LINE = re.compile(r'(x|y)=([0-9]*), [xy]=([0-9]*)\.\.([0-9]*)')


class ClayMap(UnknownMap):
    def __init__(self, input: list[str]):
        super().__init__(CLAY + WATER + FLOW)

        for line in input:
            match = LINE.match(line)
            assert match is not None, match
            if match.group(1) == 'y':
                y = int(match.group(2))
                for x in range(int(match.group(3)), int(match.group(4)) + 1):
                    self.add_feature(CLAY, Coordinate(x, y))
            else:
                x = int(match.group(2))
                for y in range(int(match.group(3)), int(match.group(4)) + 1):
                    self.add_feature(CLAY, Coordinate(x, y))

        # Add edge columns to allow water to fall there
        self.min_x -= 1
        self.max_x += 1

    def flow(self):
        self.features[WATER] = set()
        barriers = set(self.features[CLAY])

        sources = [Coordinate(500, self.min_y)]
        self.features[FLOW] = set(sources)

        while sources:
            source = sources.pop(0)

            # Flow down until a barrier (clay or still water) is reached.
            next = source.add(DOWN)
            while next not in barriers and next.y <= self.max_y and next not in self.features[FLOW]:
                source = next
                self.features[FLOW].add(source)
                next = source.add(DOWN)
            if next.y > self.max_y or next in self.features[FLOW]:
                # If we reached the bottom, this source is done.
                # If we reached moving water from another source, also done.
                continue

            # Move to the right looking for a barrier or a drop-off.
            right = source.add(RIGHT)
            while right not in barriers and right.add(DOWN) in barriers:
                self.features[FLOW].add(right)
                right = right.add(RIGHT)
            if right not in barriers:
                # Found a drop-off, add it as a source to investigate later.
                self.features[FLOW].add(right)
                sources.append(right)

            # Move to the left looking for a barrier or a drop-off.
            left = source.add(LEFT)
            while left not in barriers and left.add(DOWN) in barriers:
                self.features[FLOW].add(left)
                left = left.add(LEFT)
            if left not in barriers:
                # Found a drop-off, add it as a source to investigate later.
                self.features[FLOW].add(left)
                sources.append(left)

            # If both left and right hit barriers, then the water will settle here.
            if left in barriers and right in barriers:
                new_water = set(Coordinate(x, source.y) for x in range(left.x + 1, right.x))
                self.features[WATER].update(new_water)
                barriers.update(new_water)
                self.features[FLOW].difference_update(new_water)

                # Add the square above the current flow as a new source to investigate further
                new_source = source.add(UP)
                sources.append(new_source)
                self.features[FLOW].add(new_source)

            # Otherwise, continue on to the next source to be investigated.
            log.log(log.DEBUG, self.print_map)

        log.log(log.INFO, self.print_map)
