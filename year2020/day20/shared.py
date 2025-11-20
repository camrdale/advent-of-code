from collections import defaultdict
import math

import numpy
import numpy.typing


TILE_SIZE = 10


class Tile:
    def __init__(self, input: list[str]) -> None:
        self.id = int(input[0][5:9])
        self.tile = numpy.array([list(line) for line in input[1:]], dtype=numpy.str_)

    def clockwise_edges(self) -> tuple[str, str, str, str]:
        return (
            ''.join(self.tile[0, :]),
            ''.join(self.tile[:, TILE_SIZE-1]),
            ''.join(self.tile[TILE_SIZE-1, :])[::-1],
            ''.join(self.tile[:, 0])[::-1]
        )
    
    def counterclockwise_edges(self) -> tuple[str, str, str, str]:
        edges = self.clockwise_edges()
        return (
            edges[0][::-1],
            edges[3][::-1],
            edges[2][::-1],
            edges[1][::-1],
        )
    
    def all_edges(self) -> tuple[str, ...]:
        return self.clockwise_edges() + self.counterclockwise_edges()
    
    def edges(self, orientation: int) -> tuple[str, str, str, str]:
        assert 0 <= orientation < 8
        edges = self.clockwise_edges()
        if orientation >= 4:
            edges = self.counterclockwise_edges()
            orientation = orientation % 4
        return edges[orientation:] + edges[:orientation] # pyright: ignore[reportReturnType]

    def top_edge(self, orientation: int) -> str:
        return self.edges(orientation)[0]

    def right_edge(self, orientation: int) -> str:
        return self.edges(orientation)[1]

    def bottom_edge(self, orientation: int) -> str:
        return self.edges(orientation)[2]

    def left_edge(self, orientation: int) -> str:
        return self.edges(orientation)[3]
    
    def remove_edges(self, orig_orientation: int) -> numpy.typing.NDArray[numpy.str_]:
        orientation = orig_orientation
        tile = self.tile

        if orientation >= 4:
            tile = numpy.fliplr(tile)
            orientation = orientation % 4
        
        tile = numpy.rot90(tile, k=orientation, axes=(0,1))

        assert ''.join(tile[0, :]) == self.top_edge(orig_orientation)
        assert ''.join(tile[:, 0])[::-1] == self.left_edge(orig_orientation)
        
        return tile[1:TILE_SIZE-1,1:TILE_SIZE-1]

    @classmethod
    def arrange(cls, input: list[list[str]]) -> tuple[numpy.typing.NDArray[numpy.uint32], numpy.typing.NDArray[numpy.uint32], dict[int, Tile]]:
        tiles: dict[int, Tile] = {}
        edges: dict[str, list[int]] = defaultdict(list)
        for tile_input in input:
            tile = Tile(tile_input)
            tiles[tile.id] = tile
            for edge in tile.all_edges():
                edges[edge].append(tile.id)
        
        shape = int(math.sqrt(len(tiles)))

        arranged = numpy.zeros((shape, shape), dtype=numpy.uint32)
        for tile in tiles.values():
            num_neighbors = [
                len(set(edges[edge]) - set([tile.id]))
                for edge in tile.clockwise_edges()]
            if sum(num_neighbors) == 2:
                arranged[0, 0] = tile.id
                break
        else:
            raise ValueError(f'Failed to find a corner to start from')
        
        orientations = numpy.zeros((shape, shape), dtype=numpy.uint32)
        tile = tiles[arranged[0,0]]
        for orientation in range(4):
            if len(set(edges[tile.top_edge(orientation)]) - set([tile.id])) == 0 and len(set(edges[tile.left_edge(orientation)]) - set([tile.id])) == 0:
                orientations[0,0] = orientation
                break
        else:
            raise ValueError(f'Failed to find an orientation for starting tile')

        for x in range(1, shape):
            left_tile = tiles[arranged[x-1,0]]
            left_edge = left_tile.right_edge(orientations[x-1,0])[::-1]
            candidates = set(edges[left_edge]) - set([left_tile.id])
            assert len(candidates) == 1, candidates
            tile = tiles[next(iter(candidates))]
            arranged[x,0] = tile.id
            for orientation in range(8):
                if tile.left_edge(orientation) == left_edge and len(set(edges[tile.top_edge(orientation)]) - set([tile.id])) == 0:
                    orientations[x,0] = orientation
                    break
            else:
                raise ValueError(f'Failed to find an orientation for top edge tile: {x}')

        for y in range(1, shape):
            top_tile = tiles[arranged[0,y-1]]
            top_edge = top_tile.bottom_edge(orientations[0,y-1])[::-1]
            candidates = set(edges[top_edge]) - set([top_tile.id])
            assert len(candidates) == 1, candidates
            tile = tiles[next(iter(candidates))]
            arranged[0,y] = tile.id
            for orientation in range(8):
                if tile.top_edge(orientation) == top_edge and len(set(edges[tile.left_edge(orientation)]) - set([tile.id])) == 0:
                    orientations[0,y] = orientation
                    break
            else:
                raise ValueError(f'Failed to find an orientation for left edge tile')

        for x in range(1, shape):
            for y in range(1, shape):
                left_tile = tiles[arranged[x-1,y]]
                left_edge = left_tile.right_edge(orientations[x-1,y])[::-1]
                top_tile = tiles[arranged[x,y-1]]
                top_edge = top_tile.bottom_edge(orientations[x,y-1])[::-1]
                candidates = set(edges[left_edge]) - set([left_tile.id])
                assert len(candidates) == 1, candidates
                tile = tiles[next(iter(candidates))]
                arranged[x,y] = tile.id
                for orientation in range(8):
                    if tile.left_edge(orientation) == left_edge and tile.top_edge(orientation) == top_edge:
                        orientations[x,y] = orientation
                        break
                else:
                    raise ValueError(f'Failed to find an orientation for inner tile')

        return arranged, orientations, tiles
