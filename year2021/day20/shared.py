from aoc.map import ParsedMap, Coordinate


ONE = '#'


class ImageEnhancer(ParsedMap):
    def __init__(self, enhancement_map: str, image_input: list[str]):
        super().__init__(image_input, ONE)
        self.enhancements = 0
        self.enhancement_map = enhancement_map

    def out_of_bounds_lit(self) -> bool:
        """Returns true if an out-of-bounds pixel is currently lit."""
        return self.enhancement_map[0] == ONE and self.enhancements % 2 == 1

    def bit(self, location: Coordinate) -> int:
        """Determine the bit corresponding to a location in the image grid."""
        if self.valid(location):
            return 1 if location in self.features[ONE] else 0
        if self.out_of_bounds_lit():
            return 1
        return 0

    def enhance(self):
        new_ones: set[Coordinate] = set()
        # Loop over one additional row/column on all 4 edges of the current grid.
        for x in range(self.min_x - 1, self.max_x + 2):
            # num contains the previous row's number
            num = (2**512 - 1) if self.out_of_bounds_lit() else 0
            for y in range(self.min_y - 1, self.max_y + 2):
                # Shift in the next row's 3 values
                for next_row_x in range(x-1, x+2):
                    num <<= 1
                    num |= self.bit(Coordinate(next_row_x, y+1))
                num %= 512
                if self.enhancement_map[num] == ONE:
                    new_ones.add(Coordinate(x,y))

        # Update the grid with the new image and the expanded limits.
        self.features[ONE] = new_ones
        self.min_x -= 1
        self.min_y -= 1
        self.max_x += 1
        self.max_y += 1
        self.enhancements += 1

    def lit_pixels(self) -> int:
        if self.out_of_bounds_lit():
            raise ValueError(f'Infinite pixels are lit')
        return len(self.features[ONE])
