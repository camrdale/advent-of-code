from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate
from aoc.runner import Part

from year2020.day24.shared import HEX_NEIGHBORS, parse_tiles


def neighbors(location: Coordinate) -> list[Coordinate]:
    return [location.add(offset) for offset in HEX_NEIGHBORS.values()]


def num_black_neighbors(location: Coordinate, tiles: dict[Coordinate, bool]) -> int:
    return sum(
        tiles.get(neighbor, False)
        for neighbor in neighbors(location)
    )


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        tiles: dict[Coordinate, bool] = parse_tiles(input)

        for day in range(100):
            checked: set[Coordinate] = set()
            new_tiles: dict[Coordinate, bool] = tiles.copy()
            for tile in tiles:
                for location in [tile] + neighbors(tile):
                    if location in checked:
                        continue
                    checked.add(location)
                    black_neighbors = num_black_neighbors(location, tiles)
                    if tiles.get(location, False) and (black_neighbors == 0 or black_neighbors > 2):
                        new_tiles[location] = False
                    if not tiles.get(location, False) and black_neighbors == 2:
                        new_tiles[location] = True
            tiles = new_tiles
            log.log(log.INFO, lambda: f'Day {day+1}: {sum(tiles.values())}')

        num_black = sum(tiles.values())
        log.log(log.RESULT, f'The number of black tiles after 100 days: {num_black}')
        return num_black


part = Part2()

part.add_result(2208, """
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
""")

part.add_result(4147)
