import itertools
from typing import NamedTuple, Self

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from aoc.input import InputParser
from aoc import log
from aoc.map import Coordinate
from aoc.runner import Part


class Edge(NamedTuple):
    x: int
    start_y: int
    end_y: int

    @classmethod
    def from_vertices(cls, vertex_a: Coordinate, vertex_b: Coordinate) -> tuple[bool, Self]:
        if vertex_a.x == vertex_b.x:
            return True, cls(vertex_a.x, vertex_a.y, vertex_b.y)
        return False, cls(vertex_b.y, vertex_a.x, vertex_b.x)

    def upward(self) -> bool:
        return self.start_y < self.end_y


def is_inside(y: int, start_x: int, end_x: int, vertical_edges: list[Edge]) -> bool:
    """Determine if a horizontal line from (start_x, y) to (end_x, y) is inside."""
    possible_edges = [
        edge
        for edge in vertical_edges
        if edge.x <= end_x and (edge.start_y <= y <= edge.end_y or edge.start_y >= y >= edge.end_y)]

    inside = False
    intersecting_edges: list[tuple[bool, Edge]] = []
    i = 0
    while i < len(possible_edges):
        edge = possible_edges[i]
        if y != edge.start_y and y != edge.end_y:
            inside = not inside
            if start_x <= edge.x <= end_x:
                intersecting_edges.append((inside, edge))
        else:
            # Everything here is to handle special case of edges that overlap with the line

            if i + 1 == len(possible_edges):
                # Extra special case where this is the last edge (end of the overlapping edge is beyond our line).
                intersecting_edges.append((not inside, edge))
                break

            # Consider the directionality of two edges, and whether we start inside or outside the shape.
            i += 1
            next_edge = possible_edges[i]
            if inside:
                if edge.upward() != next_edge.upward():
                    # Opposite direction edges, so we're still inside, ignore both
                    pass
                else:
                    # inside ends at next edge, ignore this one
                    inside = False
                    if start_x <= next_edge.x <= end_x:
                        intersecting_edges.append((inside, next_edge))

            else:  # start outside
                if edge.upward() != next_edge.upward():
                    # Inside only for the duration of the overlap, so include both
                    if start_x <= edge.x <= end_x:
                        intersecting_edges.append((True, edge))
                    if start_x <= next_edge.x <= end_x:
                        intersecting_edges.append((False, next_edge))
                else:
                    # inside starts at first edge, ignore next one
                    inside = True
                    if start_x <= edge.x <= end_x:
                        intersecting_edges.append((inside, edge))

        i += 1

    for becomes_inside, intersecting_edge in intersecting_edges:
        if becomes_inside:
            if start_x < intersecting_edge.x:
                return False
        else:  # edge marks becoming outside
            if end_x > intersecting_edge.x:
                return False

    return True


def plot(vertical_edges: list[Edge], horizontal_edges: list[Edge], rectangle: tuple[Coordinate, Coordinate]):
    vertex_a, vertex_b = rectangle
    ax = plt.subplots()[1]

    # Plot the rectangle of the area between two vertices
    rect = Rectangle(
        (min(vertex_a.x, vertex_b.x), min(vertex_a.y, vertex_b.y)),
        width=abs(vertex_a.x - vertex_b.x),
        height=abs(vertex_a.y - vertex_b.y),
        edgecolor='red', facecolor='green')
    ax.add_patch(rect)

    # Add all of the lines to the plot
    for edge in vertical_edges:
        ax.plot([edge.x, edge.x], [edge.start_y, edge.end_y], color='blue', linewidth=2) 
    for edge in horizontal_edges:
        ax.plot([edge.start_y, edge.end_y], [edge.x, edge.x], color='blue', linewidth=2) 

    limit = 12 if max(vertex_a.x, vertex_b.x) < 12 else 100_000
    ax.set_xlim(0, limit)
    ax.set_ylim(0, limit)
    ax.set_aspect('equal') # Maintain aspect ratio for accurate shape representation
    plt.title('Largest Floor Tiles Area')
    plt.grid(True)
    plt.show()


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        tiles = [Coordinate.from_text(line) for line in input]

        vertical_edges: list[Edge] = []
        horizontal_edges: list[Edge] = []
        for tile_a, tile_b in list(itertools.pairwise(tiles)) + [(tiles[-1], tiles[0])]:
            vertical, edge = Edge.from_vertices(tile_a, tile_b)
            if vertical:
                vertical_edges.append(edge)
            else:
                horizontal_edges.append(edge)
        
        vertical_edges.sort()
        horizontal_edges.sort()

        possible_rectangles = [
            ((abs(tile_a.x - tile_b.x) + 1) * (abs(tile_a.y - tile_b.y) + 1), tile_a, tile_b)
            for tile_a, tile_b in itertools.combinations(tiles, 2)
        ]
        possible_rectangles.sort(reverse=True)

        for area, vertex_a, vertex_b in possible_rectangles:
            # plot(vertical_edges, horizontal_edges, (vertex_a, vertex_b))

            if not is_inside(vertex_a.y, min(vertex_a.x, vertex_b.x), max(vertex_a.x, vertex_b.x), vertical_edges):
                continue
            if not is_inside(vertex_b.y, min(vertex_a.x, vertex_b.x), max(vertex_a.x, vertex_b.x), vertical_edges):
                continue

            # While the names don't make sense, handling horizontal edges just requires swapping x/y.
            if not is_inside(vertex_a.x, min(vertex_a.y, vertex_b.y), max(vertex_a.y, vertex_b.y), horizontal_edges):
                continue
            if not is_inside(vertex_b.x, min(vertex_a.y, vertex_b.y), max(vertex_a.y, vertex_b.y), horizontal_edges):
                continue

            # plot(vertical_edges, horizontal_edges, (vertex_a, vertex_b))
            log.log(log.RESULT, f'The largest area rectangle is: {area}')
            return area
            
        raise ValueError(f'Failed to find a rectangle inside')


part = Part1()

part.add_result(24, """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
""")

part.add_result(1644094530)
