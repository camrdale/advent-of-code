import numpy
import numpy.typing

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2020.day20.shared import Tile


MONSTER = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_multipart_input()

        arranged, orientations, tiles = Tile.arrange(input)

        shape = arranged.shape[0]

        rows: list[numpy.typing.NDArray[numpy.str_]] = []
        for y in range(shape):
            rows.append(numpy.hstack([
                tiles[arranged[x, y]].remove_edges(orientations[x, y])
                for x in range(shape)
            ]))
        all_tiles = numpy.vstack(rows)
        log.log(log.DEBUG, '\n'.join(numpy.apply_along_axis(lambda row: ''.join(row), 1, all_tiles)) + '\n')

        monster_array = numpy.array([list(line) for line in MONSTER.split('\n')], dtype=numpy.str_)
        monster_indices = numpy.nonzero(monster_array == '#')

        monster_offsets: list[tuple[int, int]] = []
        num_orientations = 0
        while len(monster_offsets) == 0:
            for x in range(all_tiles.shape[0] - monster_array.shape[0]):
                for y in range(all_tiles.shape[1] - monster_array.shape[1]):
                    if (all_tiles[monster_indices[0] + x, monster_indices[1] + y] != '#').sum() == 0:
                        monster_offsets.append((x, y))
            if len(monster_offsets) == 0:
                if num_orientations == 3:
                    all_tiles = numpy.fliplr(all_tiles)
                elif num_orientations == 8:
                    raise ValueError(f'Failed to find an orientation that had monsters.')
                else:
                    all_tiles = numpy.rot90(all_tiles, k=1, axes=(0,1))
                num_orientations += 1

        for x, y in monster_offsets:
            all_tiles[monster_indices[0] + x, monster_indices[1] + y] = 'O'
        
        log.log(log.INFO, '\n'.join(numpy.apply_along_axis(lambda row: ''.join(row), 1, all_tiles)) + '\n')
        water_roughness = (all_tiles == '#').sum()

        log.log(log.RESULT, f'The water roughness of the non-monster tiles: {water_roughness}')
        return water_roughness


part = Part2()

part.add_result(273, """
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
""")

part.add_result(2495)
