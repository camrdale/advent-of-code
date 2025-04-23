from collections import defaultdict

from aoc.map import ParsedMap, Coordinate, Offset, UP, DOWN, LEFT, RIGHT, DIAGONAL_NEIGHBORS


DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
ALL_NEIGHBORS = DIRECTIONS + DIAGONAL_NEIGHBORS
TO_CHECK = {
    UP: (UP, Offset(1, -1), Offset(-1, -1)),
    DOWN: (DOWN, Offset(1, 1), Offset(-1, 1)),
    LEFT: (LEFT, Offset(-1, 1), Offset(-1, -1)),
    RIGHT: (RIGHT, Offset(1,1), Offset(1,-1))}

ELF = '#'


class ElfMap(ParsedMap):
    def __init__(self, input: list[str]):
        super().__init__(input, ELF)
        self.round_num = 0

    def no_neighbors(self, elf: Coordinate) -> bool:
        for neighbor in ALL_NEIGHBORS:
            if elf.add(neighbor) in self.features[ELF]:
                return False
        return True

    def can_move(self, elf: Coordinate, direction: Offset) -> bool:
        for to_check in TO_CHECK[direction]:
            if elf.add(to_check) in self.features[ELF]:
                return False
        return True

    def propose_move(self, elf: Coordinate) -> Coordinate | None:
        for i in range(4):
            direction = DIRECTIONS[(self.round_num + i) % len(DIRECTIONS)]
            if self.can_move(elf, direction):
                return elf.add(direction)
        return None

    def propose_moves(self) -> dict[Coordinate, list[Coordinate]]:
        proposals: dict[Coordinate, list[Coordinate]] = defaultdict(list)

        for elf in self.features[ELF]:
            if self.no_neighbors(elf):
                continue
            proposal = self.propose_move(elf)
            if proposal is not None:
                proposals[proposal].append(elf)

        return proposals
    
    def make_moves(self, proposals: dict[Coordinate, list[Coordinate]]) -> bool:
        valid_moves = [
            (proposal, elves)
            for proposal, elves in proposals.items()
            if len(elves) == 1]
        for _, elves in valid_moves:
            self.features[ELF].remove(elves[0])
        for proposal, elves in valid_moves:
            self.add_feature(ELF, proposal)
        return len(valid_moves) != 0
    
    def execute_round(self) -> bool:
        proposals = self.propose_moves()
        result = self.make_moves(proposals)
        self.round_num += 1
        return result

    def empty_tiles(self) -> int:
        min_x, max_x = self.max_x, self.min_x
        min_y, max_y = self.max_y, self.min_y
        for elf in self.features[ELF]:
            min_x = min(min_x, elf.x)
            max_x = max(max_x, elf.x)
            min_y = min(min_y, elf.y)
            max_y = max(max_y, elf.y)
        return (max_x - min_x + 1) * (max_y - min_y + 1) - len(self.features[ELF])
