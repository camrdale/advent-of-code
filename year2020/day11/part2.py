from aoc.input import InputParser
from aoc import log
from aoc.map import ParsedMap, Coordinate, NEIGHBORS, DIAGONAL_NEIGHBORS
from aoc.runner import Part


SEAT = 'L'
OCCUPIED = '#'


class Seats(ParsedMap):
    def __init__(self, lines: list[str]) -> None:
        super().__init__(lines, SEAT)
        self.occupied: set[Coordinate] = set()

        self.adjacent: dict[Coordinate, set[Coordinate]] = {}
        for seat in self.features[SEAT]:
            self.adjacent[seat] = set()
            for neighbor_offset in (NEIGHBORS + DIAGONAL_NEIGHBORS):
                neighbor = seat.add(neighbor_offset)
                while self.valid(neighbor):
                    if neighbor in self.features[SEAT]:
                        self.adjacent[seat].add(neighbor)
                        break
                    neighbor = neighbor.add(neighbor_offset)

    def iterate_once(self) -> None:
        new_occupied = self.occupied.copy()

        for seat in self.features[SEAT]:
            num_adjacent = len(self.occupied & self.adjacent[seat])
            if num_adjacent == 0:
                new_occupied.add(seat)
            elif num_adjacent >= 5:
                new_occupied.discard(seat)

        self.occupied = new_occupied
        log.log(log.DEBUG, self.print)

    def iterate_until_stable(self) -> int:
        iterations = 0
        old_hash = self.hash()
        while True:
            self.iterate_once()
            iterations += 1
            hash = self.hash()
            if hash == old_hash:
                break
            old_hash = hash
        return iterations

    def hash(self) -> int:
        return hash(frozenset(self.occupied))

    def print(self) -> str:
        return self.print_map(additional_features={OCCUPIED: self.occupied})

    def num_occupied(self) -> int:
        return len(self.occupied)


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        seats = Seats(input)

        iterations = seats.iterate_until_stable()

        log.log(log.INFO, seats.print)

        num_occupied = seats.num_occupied()
        log.log(log.RESULT, f'After {iterations} rounds the chaos stabilizes with {num_occupied} occupied seats')
        return num_occupied


part = Part1()

part.add_result(26, """
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
""")

part.add_result(1937)
