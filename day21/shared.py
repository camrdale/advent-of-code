from abc import ABC, abstractmethod
from typing import NamedTuple

import cachetools

from aoc.log import log, DEBUG

MAX_CACHE_SIZE = 2000


class Move(NamedTuple):
    source: str
    destination:str

    def reverse(self) -> 'Move':
        return Move(self.destination, self.source)


class Robot(ABC):
    def __init__(self, next_robot: 'Robot | None'=None):
        self.next_robot = next_robot
        self.cache: cachetools.LRUCache[tuple[str, str], str] = cachetools.LRUCache(maxsize=MAX_CACHE_SIZE)
    
    @abstractmethod
    def button_presses(self, current_pos: str, code: str) -> list[str]:
        pass

    @cachetools.cachedmethod(lambda self: self.cache)
    def complete_button_presses(self, code: str) -> int:
        assert code[-1] == 'A'
        num_presses = 0
        current_pos = 'A'
        for c in code:
            num_presses += self.one_button_presses(current_pos, c)
            current_pos = c
        log(DEBUG, f'{self}: for {code}, press: {num_presses}')
        return num_presses
    
    def one_button_presses(self, current_pos: str, code: str) -> int:
        assert len(code) == 1
        presses = self.button_presses(current_pos, code)
        if self.next_robot is None:
            return min(len(p) for p in presses)
        if len(presses) == 1:
            return self.next_robot.complete_button_presses(presses[0])
        log(DEBUG, f'to get to {code} from {current_pos}, choosing between {presses}')
        press_lengths: list[tuple[int, str]] = []
        for p in presses:
            next_presses = self.next_robot.complete_button_presses(p)
            log(DEBUG, f'press {p} results in length {next_presses}: {next_presses}')
            press_lengths.append((next_presses, p))
        press_lengths.sort()
        return self.next_robot.complete_button_presses(press_lengths[0][1])
    
    @staticmethod
    def reverse_presses(presses: str) -> str:
        reversed_presses = ''
        for code in reversed(presses):
            if code == '>':
                reversed_presses += '<'
            elif code == '<':
                reversed_presses += '>'
            elif code == '^':
                reversed_presses += 'v'
            elif code == 'v':
                reversed_presses += '^'
            else:
                assert False
        return reversed_presses


class NumericalRobot(Robot):
    def __init__(self, next_robot: 'Robot | None'=None):
        super().__init__(next_robot)
        self.moves: dict[Move, list[str]] = {}

        # Moves from 0-9 to a larger number
        for source in range(0, 9):
            source_coord = NumericalRobot.row_and_column(str(source))
            for destination in range(source + 1, 10):
                destination_coord = NumericalRobot.row_and_column(str(destination))
                presses = '^'*(destination_coord[0] - source_coord[0])
                if source_coord[1] < destination_coord[1]:
                    presses += '>'*(destination_coord[1] - source_coord[1])
                else:
                    presses += '<'*(source_coord[1] - destination_coord[1])
                possibilities = [presses]
                if source != 0 or destination_coord[1] != 0:
                    # Can't use this for '0' to first column as it would cross the empty grid square
                    possibilities.append(presses[::-1])
                self.moves[Move(str(source), str(destination))] = possibilities

        # Moves from A to a number
        self.moves[Move('A', '0')] = ['<']
        source_coord = NumericalRobot.row_and_column('A')
        for destination in range(1, 10):
            destination_coord = NumericalRobot.row_and_column(str(destination))
            presses = '^'*(destination_coord[0] - source_coord[0])
            if source_coord[1] < destination_coord[1]:
                presses += '>'*(destination_coord[1] - source_coord[1])
            else:
                presses += '<'*(source_coord[1] - destination_coord[1])
            possibilities = [presses]
            if destination_coord[1] != 0:
                # Can't use this for 'A' to first column as it would cross the empty grid square
                possibilities.append(presses[::-1])
            self.moves[Move('A', str(destination))] = possibilities

        # All the remaining moves that are existing moves in reverse
        for move, presses in list(self.moves.items()):
            self.moves[move.reverse()] = [Robot.reverse_presses(p) for p in presses] 
        
        # No-op moves
        for code in list(map(str, range(0, 10))) + ['A']:
            self.moves[Move(code, code)] = ['']
        
        assert len(self.moves) == 11 * 11

        # Add A to the end of all moves
        for move, presses in self.moves.items():
            self.moves[move] = [p + 'A' for p in presses]

    @staticmethod
    def row_and_column(code: str) -> tuple[int, int]:
        if code == '0':
            return 0, 1
        if code == 'A':
            return 0, 2
        code_num = int(code)
        row = (code_num + 2) // 3
        column = (code_num - 1) % 3
        return row, column

    def button_presses(self, current_pos: str, code: str) -> list[str]:
        assert len(code) == 1
        return self.moves[Move(current_pos, code)]


class DirectionalRobot(Robot):
    def __init__(self, next_robot: 'Robot | None'=None):
        super().__init__(next_robot)
        self.moves: dict[Move, list[str]] = {
            Move('A', '^'): ['<'],
            Move('A', '>'): ['v'],
            Move('A', 'v'): ['v<', '<v'],
            Move('A', '<'): ['v<<', '<v<'],
            Move('^', '>'): ['v>', '>v'],
            Move('^', 'v'): ['v'],
            Move('^', '<'): ['v<'],
            Move('>', 'v'): ['<'],
            Move('>', '<'): ['<<'],
            Move('v', '<'): ['<'],
        }

        # All the remaining moves that are existing moves in reverse
        for move, presses in list(self.moves.items()):
            self.moves[move.reverse()] = [Robot.reverse_presses(p) for p in presses]
        
        # No-op moves
        for code in 'A<>^v':
            self.moves[Move(code, code)] = ['']
        
        assert len(self.moves) == 5 * 5

        # Add A to the end of all moves
        for move, presses in self.moves.items():
            self.moves[move] = [p + 'A' for p in presses]

    def button_presses(self, current_pos: str, code: str) -> list[str]:
        assert len(code) == 1
        return self.moves[Move(current_pos, code)]
