import queue

import aoc.input
from aoc import log
import aoc.map
from aoc import runner

from year2019 import intcode


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()
        intcode_input = list(map(int, input[0].split(',')))

        program = intcode.Program('INTCODE', list(intcode_input))
        
        program_input: queue.Queue[int] = queue.Queue()
        program_output: queue.Queue[int] = queue.Queue()

        program.execute(program_input, program_output)
        program.join()

        max_x = 0
        max_y = 0
        wall_tiles: set[aoc.map.Coordinate] = set()
        block_tiles: set[aoc.map.Coordinate] = set()
        paddle_tiles: set[aoc.map.Coordinate] = set()
        ball_tiles: set[aoc.map.Coordinate] = set()
        while not program_output.empty():
            x = program_output.get_nowait()
            y = program_output.get_nowait()
            tile_id = program_output.get_nowait()
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            location = aoc.map.Coordinate(x,y)
            if tile_id == 1:
                wall_tiles.add(location)
            else:
                wall_tiles.discard(location)
            if tile_id == 2:
                block_tiles.add(location)
            else:
                block_tiles.discard(location)
            if tile_id == 3:
                paddle_tiles.add(location)
            else:
                paddle_tiles.discard(location)
            if tile_id == 4:
                ball_tiles.add(location)
            else:
                ball_tiles.discard(location)
        
        screen = aoc.map.EmptyMap(max_x + 1, max_y + 1)
        log.log(log.INFO, screen.print_map({
            u'\u2588': wall_tiles,
            u'\u2592': block_tiles,
            '=': paddle_tiles,
            'O': ball_tiles,
        }))

        log.log(log.RESULT, f'There are {len(block_tiles)} on the screen')
        return len(block_tiles)


part = Part1()

part.add_result(306)
