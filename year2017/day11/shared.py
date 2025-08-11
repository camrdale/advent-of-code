from aoc.map import Coordinate, Offset


# Offsets to neighbors in a hexagonal grid (flat top)
# Uses double-height coordinate system:
# https://www.redblobgames.com/grids/hexagons/#coordinates-doubled
HEX_NEIGHBORS = {
    'n': Offset(0, -2),
    's': Offset(0, 2),
    'ne': Offset(1, -1),
    'se': Offset(1, 1),
    'nw': Offset(-1, -1),
    'sw': Offset(-1, 1),
}


def hex_distance(hex_location: Coordinate) -> int:
    """Calculates the distance from the origin of a coordinate in a double-height hex grid."""
    return max(abs(hex_location.x), (abs(hex_location.x) + abs(hex_location.y)) // 2)
