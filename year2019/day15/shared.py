import queue

from aoc import log
import aoc.map

from year2019 import intcode

DIRECTION_TO_COMMAND = {
    aoc.map.Direction.NORTH: 1,
    aoc.map.Direction.SOUTH: 2,
    aoc.map.Direction.WEST: 3,
    aoc.map.Direction.EAST: 4,
}

STATUS_WALL = 0
STATUS_MOVED = 1
STATUS_OXYGEN = 2

WALL = '#'
OPEN = ' '
OXYGEN = 'O'


class AreaMap(aoc.map.UnknownMap):
    def __init__(self, intcode_input: list[int]):
        super().__init__()
        self.intcode_input = intcode_input
        self.save_features = WALL + OPEN + OXYGEN
        self.starting_point = aoc.map.Coordinate(0,0)
        self.add_feature(OPEN, self.starting_point)

    def explore(self) -> aoc.map.Coordinate:
        """Explore the map from the origin, returning the found Oxygen location."""
        discovered: set[aoc.map.Coordinate] = set([self.starting_point])
        to_investigate: dict[aoc.map.Coordinate, tuple[aoc.map.Coordinate, intcode.ProgramState]] = {}
        for neighbor in self.starting_point.neighbors():
            to_investigate[neighbor] = self.starting_point, intcode.ProgramState.initial_state(list(self.intcode_input))

        droid_starts = 0
        while to_investigate:
            # Choose a previously undiscovered location to start from,
            # and load the program state at its discovered neighbor.
            current_location, program_state = to_investigate[next(iter(to_investigate))]
            droid = intcode.Program.from_state(f'DROID-{droid_starts}', program_state)
            droid_starts += 1
            droid_input: queue.Queue[int] = queue.Queue()
            droid_output: queue.Queue[int] = queue.Queue()
            droid.execute(droid_input, droid_output)

            # Choose a neighbor location that is undiscovered.
            next_undiscovered = [
                neighbor for neighbor in current_location.neighbors()
                if neighbor not in discovered]
            while next_undiscovered:
                # Go in the direction of the undiscovered location.
                next_location = next_undiscovered[0]
                current_direction = aoc.map.Direction.from_offset(
                    next_location.difference(current_location))
                droid_input.put(DIRECTION_TO_COMMAND[current_direction])
                status = droid_output.get()
                while status != STATUS_WALL:
                    current_location = current_location.add(current_direction.offset())
                    self.add_feature(OPEN if status == STATUS_MOVED else OXYGEN, current_location)
                    discovered.add(current_location)
                    del to_investigate[current_location]
                    for neighbor in current_location.neighbors():
                        if neighbor not in discovered:
                            to_investigate[neighbor] = current_location, droid.current_state()
                    # Stop if the next location in this direction was already discovered.
                    if current_location.add(current_direction.offset()) in discovered:
                        break
                    droid_input.put(DIRECTION_TO_COMMAND[current_direction])
                    status = droid_output.get()
                else:
                    # Hit a wall
                    blocked_location = current_location.add(current_direction.offset())
                    self.add_feature(WALL, blocked_location)
                    discovered.add(blocked_location)
                    del to_investigate[blocked_location]

                # Choose a new neighbor location that is undiscovered.
                next_undiscovered = [
                    neighbor for neighbor in current_location.neighbors()
                    if neighbor not in discovered]

            log.log(log.INFO, self.print_map(additional_features={'S': set([self.starting_point])}))

        if len(self.features[OXYGEN]) != 1:
            raise ValueError(f'Failed to find a single Oxygen location')
        return next(iter(self.features[OXYGEN]))
