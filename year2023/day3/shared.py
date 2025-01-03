import string

from aoc.map import ParsedMap, Coordinate, Offset


class PartNumberMap(ParsedMap):
    def __init__(self, input: list[str]):
        symbols = set(c for c in string.punctuation if c != '.')
        super().__init__(input, ''.join(symbols) + string.digits)
        self.input = input

        self.symbol_locations: set[Coordinate] = set()
        for feature, coords in self.features.items():
            if feature in symbols:
                self.symbol_locations.update(coords)
        self.number_locations: set[Coordinate] = set()
        for feature, coords in self.features.items():
            if feature in string.digits:
                self.number_locations.update(coords)

    def get_location(self, location: Coordinate) -> str:
        return self.input[location.y][location.x]

    def part_number_locations(self) -> set[Coordinate]:
        part_numbers: set[Coordinate] = set()
        for number_location in self.number_locations:
            all_neighbors: set[Coordinate] = set()
            all_neighbors.update(number_location.neighbors())
            all_neighbors.update(number_location.diagonal_neighbors())
            if len(all_neighbors.intersection(self.symbol_locations)) > 0:
                part_numbers.add(number_location)
        return part_numbers
    
    def get_part_number(self, starting_location: Coordinate) -> tuple[int, set[Coordinate]]:
        full_part_number = self.get_location(starting_location)
        used_locations: set[Coordinate] = set([starting_location])

        next_offset = Offset(1, 0)
        location = starting_location.add(next_offset)
        while location.valid(self.width, self.height) and location in self.number_locations:
            full_part_number += self.get_location(location)
            used_locations.add(location)
            location = location.add(next_offset)

        previous_offset = Offset(-1, 0)
        location = starting_location.add(previous_offset)
        while location.valid(self.width, self.height) and location in self.number_locations:
            full_part_number = self.get_location(location) + full_part_number
            used_locations.add(location)
            location = location.add(previous_offset)

        return int(full_part_number), used_locations
    
    def get_gears(self) -> list[tuple[int, int]]:
        gear_part_numbers: list[tuple[int, int]] = []
        possible_gears = self.features['*']
        part_numbers = self.part_number_locations()
        for possible_gear in possible_gears:
            all_neighbors: set[Coordinate] = set()
            all_neighbors.update(possible_gear.neighbors())
            all_neighbors.update(possible_gear.diagonal_neighbors())

            neighbor_part_numbers = all_neighbors.intersection(part_numbers)
            gear_numbers: list[int] = []
            while len(neighbor_part_numbers) > 0:
                part_number = next(iter(neighbor_part_numbers))
                full_part_number, used_part_numbers = self.get_part_number(part_number)
                neighbor_part_numbers -= used_part_numbers
                gear_numbers.append(full_part_number)
            
            if len(gear_numbers) == 2:
                gear_part_numbers.append((gear_numbers[0], gear_numbers[1]))

        return gear_part_numbers

