import queue

import aoc.map


class GardenMap(aoc.map.ParsedMap):
    def __init__(self, input: list[str]):
        super().__init__(input, '#S')
        self.starting_point = next(iter(self.features['S']))
        del self.features['S']

    def reachable_plots(
            self,
            starting_point: aoc.map.Coordinate,
            num_steps: int
            ) -> set[aoc.map.Coordinate]:
        visited: dict[aoc.map.Coordinate, int] = {}
        reachable: set[aoc.map.Coordinate] = set()
        paths_to_try: queue.PriorityQueue[aoc.map.Path] = queue.PriorityQueue()
        paths_to_try.put(aoc.map.Path(0, starting_point, frozenset()))

        while not paths_to_try.empty():
            path = paths_to_try.get()
            if path.length > num_steps:
                break
            if path.location in visited:
                continue
            visited[path.location] = path.length
            if (path.length % 2) == (num_steps % 2):
                reachable.add(path.location)

            for next_path in path.next_paths():
                if self.valid(next_path.location) and next_path.location not in self.features['#']:
                    paths_to_try.put(next_path)

        return reachable
