from aoc.input import InputParser
from aoc.log import log, RESULT, DEBUG
from aoc.map import ParsedMap, Offset
from aoc.runner import Part

ROUNDED = 'O'
CUBE = '#'
NORTH = Offset(0, -1)
WEST = Offset(-1, 0)
SOUTH = Offset(0, 1)
EAST = Offset(1, 0)


class RockMap(ParsedMap):
    def __init__(self, parser: InputParser):
        super().__init__(parser.get_input(), ROUNDED + CUBE)

    def total_load(self) -> int:
        load = 0
        for rock in self.features[ROUNDED]:
            load += self.height - rock.y
        return load

    def spin(self) -> None:
        rounded_rocks = sorted(self.features[ROUNDED])
        for rock in rounded_rocks:
            self.features[ROUNDED].remove(rock)
            while True:
                moved_rock = rock.add(NORTH)
                if self.valid(moved_rock) and moved_rock not in self.features[ROUNDED] and moved_rock not in self.features[CUBE]:
                    rock = moved_rock
                else:
                    break
            self.features[ROUNDED].add(rock)

        rounded_rocks = sorted(self.features[ROUNDED])
        for rock in rounded_rocks:
            self.features[ROUNDED].remove(rock)
            while True:
                moved_rock = rock.add(WEST)
                if self.valid(moved_rock) and moved_rock not in self.features[ROUNDED] and moved_rock not in self.features[CUBE]:
                    rock = moved_rock
                else:
                    break
            self.features[ROUNDED].add(rock)

        rounded_rocks = sorted(self.features[ROUNDED], reverse=True)
        for rock in rounded_rocks:
            self.features[ROUNDED].remove(rock)
            while True:
                moved_rock = rock.add(SOUTH)
                if self.valid(moved_rock) and moved_rock not in self.features[ROUNDED] and moved_rock not in self.features[CUBE]:
                    rock = moved_rock
                else:
                    break
            self.features[ROUNDED].add(rock)

        rounded_rocks = sorted(self.features[ROUNDED], reverse=True)
        for rock in rounded_rocks:
            self.features[ROUNDED].remove(rock)
            while True:
                moved_rock = rock.add(EAST)
                if self.valid(moved_rock) and moved_rock not in self.features[ROUNDED] and moved_rock not in self.features[CUBE]:
                    rock = moved_rock
                else:
                    break
            self.features[ROUNDED].add(rock)

        log(DEBUG, self.print_map())
    
    def hash_rounded(self) -> int:
        return hash(frozenset(self.features[ROUNDED]))


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        map = RockMap(parser)

        resulting_positions: dict[int, int] = {map.hash_rounded(): 0}
        resulting_loads: dict[int, int] = {0: map.total_load()}

        i = 0
        while True:
            i += 1
            map.spin()
            positions = map.hash_rounded()
            if positions in resulting_positions:
                break
            resulting_positions[positions] = i
            resulting_loads[i] = map.total_load()

        previous_i = resulting_positions[positions]
        loop_length = i - previous_i
        position_of_1B = (1000000000 - previous_i) % loop_length
        load = resulting_loads[previous_i + position_of_1B]
        log(RESULT, f'Found a loop of length {loop_length} after {i} spins, 1B should occur in position {position_of_1B} of the loop, with load: {load}')
        return load


part = Part2()

part.add_result(64, """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
""")

part.add_result(96003)
