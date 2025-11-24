from aoc.map import Coordinate, Offset


# Offsets to neighbors in a hexagonal grid (pointy top)
# Uses double-height coordinate system:
# https://www.redblobgames.com/grids/hexagons/#coordinates-doubled
HEX_NEIGHBORS = {
    'e': Offset(2, 0),
    'w': Offset(-2, 0),
    'ne': Offset(1, -1),
    'se': Offset(1, 1),
    'nw': Offset(-1, -1),
    'sw': Offset(-1, 1),
}


def parse_tiles(input: list[str]) -> dict[Coordinate, bool]:
    tiles: dict[Coordinate, bool] = {}
    for line in input:
        hex_location = Coordinate(0, 0)
        i = 0
        while i < len(line):
            if line[i] in HEX_NEIGHBORS:
                hex_location = hex_location.add(HEX_NEIGHBORS[line[i]])
                i += 1
            else:
                hex_location = hex_location.add(HEX_NEIGHBORS[line[i:i+2]])
                i += 2
        tiles[hex_location] = not tiles.get(hex_location, False)
    return tiles
