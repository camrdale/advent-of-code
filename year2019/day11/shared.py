import queue
import threading

from aoc import log
import aoc.map


class HullPaintingRobot(threading.Thread):
    def __init__(self, name: str, input: queue.Queue[int], output: queue.Queue[int], starting_color: int):
        super().__init__(name=name, daemon=True)
        self.input = input
        self.output = output
        self.location = aoc.map.Coordinate(0,0)
        self.direction_num = aoc.map.NEIGHBORS.index(aoc.map.UP)
        self.painted_white: set[aoc.map.Coordinate] = set()
        if starting_color == 1:
            self.painted_white.add(self.location)
        self.painted: set[aoc.map.Coordinate] = set()

    def run(self) -> None:
        log.log(log.INFO, f'{self.name}: is starting')
        num_commands = 0
        while True:
            current_color = 1 if self.location in self.painted_white else 0
            self.output.put(current_color)
            new_color = self.input.get()
            if new_color == -1:
                break
            turn = self.input.get()
            if turn == -1:
                break

            log.log(log.DEBUG, f'Received command to paint {self.location} {"white" if new_color else "black"} then turn {"right" if turn else "left"}')
            num_commands += 1
            self.painted.add(self.location)
            if new_color == 1:
                self.painted_white.add(self.location)
            else:
                self.painted_white.discard(self.location)
            
            if turn == 1:
                self.direction_num = (self.direction_num + 1) % 4
            else:
                self.direction_num = (self.direction_num - 1) % 4
            direction = aoc.map.NEIGHBORS[self.direction_num]
            self.location = self.location.add(direction)

        log.log(log.INFO, f'{self.name}: is done, ran {num_commands} painting commands')
