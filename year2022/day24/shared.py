from aoc import log
from aoc.map import ParsedMap, Coordinate, NEIGHBORS


EXPEDITION = 'E'


class BlizzardMap(ParsedMap):
    def __init__(self, input: list[str]):
        super().__init__(input, EXPEDITION + '#><v^')
        self.minute = 0

        # index of list is the column, set contains the rows that have blizzards for that column.
        self.blizzards_right: list[set[int]] = [set() for _ in range(self.max_x)]
        self.blizzards_left: list[set[int]] = [set() for _ in range(self.max_x)]
        for location in self.features['>']:
            self.blizzards_right[location.x].add(location.y)
        for location in self.features['<']:
            self.blizzards_left[location.x].add(location.y)

        # index of list is the row, set contains the columns that have blizzards for that row.
        self.blizzards_down: list[set[int]] = [set() for _ in range(self.max_y)]
        self.blizzards_up: list[set[int]] = [set() for _ in range(self.max_y)]
        for location in self.features['v']:
            self.blizzards_down[location.y].add(location.x)
        for location in self.features['^']:
            self.blizzards_up[location.y].add(location.x)

        # TODO: replace these with lists of 128-bit integers, with the index in the
        # list always as the row. Still use popping/inserting for the up/down blizzards.
        # But use bit shifting for the left/right blizzards. Then the 4 lists can be
        # combined by ORing the 128-bit integers togeher for each row.

    def iterate_blizzards(self):
        # Pop the end columns off and put them at the other end.
        last_col = self.blizzards_right.pop()
        self.blizzards_right.insert(1, last_col)
        first_col = self.blizzards_left.pop(1)
        self.blizzards_left.append(first_col)
        # Pop the end rows off and put them at the other end.
        last_row = self.blizzards_down.pop()
        self.blizzards_down.insert(1, last_row)
        first_row = self.blizzards_up.pop(1)
        self.blizzards_up.append(first_row)
    
    def move_expeditions(self):
        valid_positions: set[Coordinate] = set([Coordinate(1, 0), Coordinate(self.max_x-1, self.max_y)])
        for x in range(1, self.max_x):
            for y in range(1, self.max_y):
                if (y not in self.blizzards_right[x] and y not in self.blizzards_left[x]
                    and x not in self.blizzards_down[y] and x not in self.blizzards_up[y]):
                    valid_positions.add(Coordinate(x,y))

        new_expeditions: set[Coordinate] = set(self.features[EXPEDITION])
        for expedition in self.features[EXPEDITION]:
            for move in NEIGHBORS:
                new_expeditions.add(expedition.add(move))
        self.features[EXPEDITION] = new_expeditions.intersection(valid_positions)

    def shortest_path(self, starting_point: Coordinate, ending_point: Coordinate) -> int:
        self.features[EXPEDITION] = set([starting_point])
        while ending_point not in self.features[EXPEDITION]:
            self.iterate_blizzards()
            self.move_expeditions()
            self.minute += 1
            log.log(log.INFO, f'After {self.minute} minutes, there are {len(self.features[EXPEDITION])} expedition paths.')
            if log.get_log_level() >= log.DEBUG:
                self.features['>'] = set([Coordinate(x,y) for x, rows in enumerate(self.blizzards_right) for y in rows])
                self.features['<'] = set([Coordinate(x,y) for x, rows in enumerate(self.blizzards_left) for y in rows])
                self.features['v'] = set([Coordinate(x,y) for y, columns in enumerate(self.blizzards_down) for x in columns])
                self.features['^'] = set([Coordinate(x,y) for y, columns in enumerate(self.blizzards_up) for x in columns])
                log.log(log.DEBUG, self.print_map())
        return self.minute
