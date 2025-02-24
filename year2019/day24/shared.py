from typing import NamedTuple

from aoc.map import ParsedMap, Coordinate


def to_map(biodiversity: int) -> list[str]:
    s: list[str] = []
    for y in range(5):
        s.append('')
        for x in range(5):
            num = y * 5 + x
            bit_mask = 1 << num
            if bit_mask & biodiversity:
                s[-1] += '#'
            else:
                s[-1] += '.'
    return s


class BitMasks(NamedTuple):
    bit_mask: int
    adjacent_mask: int
    adjacent_mask_above: int
    adjacent_mask_below: int


def parse_and_build_bit_masks(input: list[str]) -> tuple[int, dict[int, BitMasks]]:
    map = ParsedMap(input, '#')
    bit_masks: dict[int, BitMasks] = {}
    biodiversity = 0
    for y in range(5):
        for x in range(5):
            num = y * 5 + x
            bit_mask = 1 << num
            adjacent_mask = 0
            adjacent_mask_above = 0
            adjacent_mask_below = 0
            if x > 0:
                adjacent_mask |= 1 << (num - 1)
            if y > 0:
                adjacent_mask |= 1 << (num - 5)
            if x < 4:
                adjacent_mask |= 1 << (num + 1)
            if y < 4:
                adjacent_mask |= 1 << (num + 5)
            if num == 11:
                adjacent_mask_below |= (1 | 1 << 5 | 1 << 10 | 1 << 15 | 1 << 20)
            if num == 7:
                adjacent_mask_below |= (1 | 1 << 1 | 1 << 2 | 1 << 3 | 1 << 4)
            if num == 13:
                adjacent_mask_below |= (1 << 4 | 1 << 9 | 1 << 14 | 1 << 19 | 1 << 24)
            if num == 17:
                adjacent_mask_below |= (1 << 20 | 1 << 21 | 1 << 22 | 1 << 23 | 1 << 24)
            if x == 0:
                adjacent_mask_above |= 1 << 11
            if x == 4:
                adjacent_mask_above |= 1 << 13
            if y == 0:
                adjacent_mask_above |= 1 << 7
            if y == 4:
                adjacent_mask_above |= 1 << 17
            bit_masks[num] = BitMasks(bit_mask, adjacent_mask, adjacent_mask_above, adjacent_mask_below)
            if Coordinate(x,y) in map.features['#']:
                biodiversity += bit_mask
    return biodiversity, bit_masks
