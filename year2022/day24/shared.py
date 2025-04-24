from aoc import log
from aoc.map import ParsedMap, Coordinate


class BlizzardMap(ParsedMap):
    def __init__(self, input: list[str]):
        super().__init__(input, 'E#><v^')
        self.minute = 0

        # Lists of 128-bit integers (actually arbitrarily large), with the index in the
        # list always as the row. Blizzards are in columns with set bits in the number.
        # Ignore the bottom row as no blizzard can be there.
        self.blizzards_right = [0 for _ in range(self.max_y)]
        self.blizzards_left = [0 for _ in range(self.max_y)]
        self.blizzards_down = [0 for _ in range(self.max_y)]
        self.blizzards_up = [0 for _ in range(self.max_y)]
        for location in self.features['>']:
            self.blizzards_right[location.y] |= 1<<location.x
        for location in self.features['<']:
            self.blizzards_left[location.y] |= 1<<location.x
        for location in self.features['v']:
            self.blizzards_down[location.y] |= 1<<location.x
        for location in self.features['^']:
            self.blizzards_up[location.y] |= 1<<location.x

        # Same for walls, but with an extra row for the bottom wall.
        self.walls = [0 for _ in range(self.max_y + 1)]
        for location in self.features['#']:
            self.walls[location.y] |= 1<<location.x

        self.last_col_mask = 1<<(self.max_x-1)

    def iterate_blizzards(self):
        # For left/right moving blizzards, bit shift the left/right columns to the other end.
        for y in range(1, self.max_y):
            last_col = self.blizzards_right[y] & self.last_col_mask
            self.blizzards_right[y] = (self.blizzards_right[y] << 1) | (2 if last_col else 0)
            first_col = self.blizzards_left[y] & 2
            self.blizzards_left[y] = (self.blizzards_left[y] >> 1) | (self.last_col_mask if first_col else 0)

        # For up/down moving blizzards, pop the end rows off and put them at the other end.
        last_row = self.blizzards_down.pop()
        self.blizzards_down.insert(1, last_row)
        first_row = self.blizzards_up.pop(1)
        self.blizzards_up.append(first_row)
    
    def move_expeditions(self):
        # OR together the blizzards and walls for each row.
        unavailable = [
            self.blizzards_left[y] | self.blizzards_right[y] | self.blizzards_down[y] | self.blizzards_up[y] | self.walls[y]
            for y in range(self.max_y)]
        unavailable.append(self.walls[self.max_y])

        new_expeditions: list[int] = []
        for y in range(self.max_y + 1):
            # Waiting in place
            new_expedition = self.expeditions[y]
            if y > 0:
                # Expeditions above can move into this row.
                new_expedition |= self.expeditions[y-1]
            if y < self.max_y:
                # Expeditions below can move into this row.
                new_expedition |= self.expeditions[y+1]
            # Expeditions in this row can move right (clear the bit for the column on the far left)
            new_expedition |= (self.expeditions[y] << 1) & (~2)
            # Expeditions in this row can move left (clear the bit for the column on the far right)
            new_expedition |= (self.expeditions[y] >> 1) & (~self.last_col_mask)
            # Remove any squares that are unavailable due to blizzards/walls.
            new_expedition &= ~unavailable[y]

            new_expeditions.append(new_expedition)
        self.expeditions = new_expeditions

    def shortest_path(self, starting_point: Coordinate, ending_point: Coordinate) -> int:
        # Also store possible expeditions in a list of integers, same as walls/blizzards.
        self.expeditions = [0 for _ in range(self.max_y + 1)]
        self.expeditions[starting_point.y] |= 1<<starting_point.x
        
        while not (self.expeditions[ending_point.y] & 1<<ending_point.x):
            self.iterate_blizzards()
            self.move_expeditions()
            self.minute += 1
            if log.get_log_level() >= log.INFO:
                self.features['E'] = set([Coordinate(x,y) for y, columns in enumerate(self.expeditions) for x in range(1, self.max_x + 1) if 1<<x & columns])
                log.log(log.INFO, f'After {self.minute} minutes, there are {len(self.features["E"])} expedition paths.')
            if log.get_log_level() >= log.DEBUG:
                self.features['>'] = set([Coordinate(x,y) for y, columns in enumerate(self.blizzards_right) for x in range(1, self.max_x) if 1<<x & columns])
                self.features['<'] = set([Coordinate(x,y) for y, columns in enumerate(self.blizzards_left) for x in range(1, self.max_x) if 1<<x & columns])
                self.features['v'] = set([Coordinate(x,y) for y, columns in enumerate(self.blizzards_down) for x in range(1, self.max_x) if 1<<x & columns])
                self.features['^'] = set([Coordinate(x,y) for y, columns in enumerate(self.blizzards_up) for x in range(1, self.max_x) if 1<<x & columns])
                log.log(log.DEBUG, self.print_map())
        return self.minute
