import queue
import threading

import aoc.input
from aoc import log
import aoc.map
from aoc import runner

from year2019 import intcode

WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4
SCORE = -1


class BreakoutPlayer(threading.Thread):
    def __init__(self, name: str, input: queue.Queue[int], output: queue.Queue[int]):
        super().__init__(name=name, daemon=True)
        self.input = input
        self.output = output
        self.max_x = 0
        self.max_y = 0
        self.wall_tiles: set[aoc.map.Coordinate] = set()
        self.block_tiles: set[aoc.map.Coordinate] = set()
        self.paddle_tiles: set[aoc.map.Coordinate] = set()
        self.ball_tiles: set[aoc.map.Coordinate] = set()
        self.score = -1
        self.initialized = False

    def update_tile(self, location: aoc.map.Coordinate, tile_id: int) -> None:
        if tile_id == WALL:
            self.wall_tiles.add(location)
        else:
            self.wall_tiles.discard(location)
        if tile_id == BLOCK:
            self.block_tiles.add(location)
        else:
            self.block_tiles.discard(location)
        if tile_id == PADDLE:
            self.paddle_tiles.add(location)
        else:
            self.paddle_tiles.discard(location)
        if tile_id == BALL:
            self.ball_tiles.add(location)
        else:
            self.ball_tiles.discard(location)

    def get_updates_until(self, return_on_update: int) -> None:
        while True:
            x = self.input.get()
            y = self.input.get()
            tile_id = self.input.get()
            if x == -1 and y == 0:
                self.score = tile_id
                log.log(log.DEBUG, f'{self.name} updated score: {self.score}')
                if not self.initialized:
                    self.initialized = True
                if return_on_update == SCORE:
                    break
                else:
                    continue
            log.log(log.DEBUG, f'  {self.name} {tile_id} at ({x},{y})')
            if x > self.max_x:
                self.max_x = x
            if y > self.max_y:
                self.max_y = y
            location = aoc.map.Coordinate(x,y)
            self.update_tile(location, tile_id)
            if tile_id == return_on_update or (self.initialized and not self.block_tiles):
                break

        screen = aoc.map.EmptyMap(self.max_x + 1, self.max_y + 1)
        log.log(log.INFO, screen.print_map({
            u'\u2588': self.wall_tiles,
            u'\u2592': self.block_tiles,
            '=': self.paddle_tiles,
            'O': self.ball_tiles,
        }))
        log.log(log.INFO, f'Score: {self.score}')

    def run(self) -> None:
        log.log(log.INFO, f'{self.name}: is starting')
        num_moves = 0
        self.get_updates_until(SCORE)
        while self.block_tiles:
            if len(self.ball_tiles) != 1:
                raise ValueError(f'Expected 1 ball tile, got: {self.ball_tiles}')
            if len(self.paddle_tiles) != 1:
                raise ValueError(f'Expected 1 paddle tile, got: {self.paddle_tiles}')
            ball = next(iter(self.ball_tiles))
            paddle = next(iter(self.paddle_tiles))
            if ball.x < paddle.x:
                self.output.put(-1)
                num_moves += 1
            elif ball.x > paddle.x:
                self.output.put(1)
                num_moves += 1
            else:
                self.output.put(0)
                num_moves += 1
            self.get_updates_until(BALL)

        self.get_updates_until(SCORE)
        log.log(log.INFO, f'{self.name}: is done, made {num_moves} joystick moves')


class Part2(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))

        intcode_input[0] = 2
        program = intcode.Program('BREAKOUT', list(intcode_input))
        
        program_input: queue.Queue[int] = queue.Queue()
        program_output: queue.Queue[int] = queue.Queue()

        player = BreakoutPlayer('PLAYER', program_output, program_input)
        player.start()

        program.execute(program_input, program_output)

        player.join()
        program.join()

        log.log(log.RESULT, f'Score after breaking all the blocks: {player.score}')
        return player.score


part = Part2()

part.add_result(15328)
