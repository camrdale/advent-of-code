#!/usr/bin/python

import math
from collections.abc import Iterable, Iterator
from pathlib import Path

INPUT_FILE = Path(__file__).parent.resolve() / 'input.txt'
TEST_INPUT = '125 17'


class Stone:
    def __init__(self, value: int, next_stone: 'Stone | None'):
        self.value = value
        self.next = next_stone
    
    def splittable(self) -> bool:
        return (math.floor(math.log10(self.value)) + 1) % 2 == 0
    
    def split(self) -> None:
        s = str(self.value)
        n = len(s) // 2
        self.next = Stone(int(s[n:]), self.next)
        self.value = int(s[:n])
    
    def blink(self) -> None:
        if self.value == 0:
            self.value = 1
        elif self.splittable():
            self.split()
        else:
            self.value *= 2024

    def __str__(self) -> str:
        return str(self.value)


class StoneArrangement:
    def __init__(self, stones: Iterable[str]):
        self.head_stone: Stone | None = None
        for value in reversed(list(map(int, stones))):
            self.head_stone = Stone(value, self.head_stone)

    def stones(self) -> Iterator[Stone]:
        stone = self.head_stone
        while stone is not None:
            next_stone = stone.next
            yield stone
            stone = next_stone

    def num_stones(self) -> int:
        return sum(1 for _ in self.stones())

    def blink(self) -> None:
        for stone in self.stones():
            stone.blink()
    
    def __str__(self) -> str:
        return 'StoneArrangement(' + ', '.join(str(stone) for stone in self.stones()) + ')'


def main():
    with INPUT_FILE.open() as ifp:
        arrangement = StoneArrangement(
                # TEST_INPUT.split()
                ifp.readline().strip().split()
        )

    # print(arrangement)
    for i in range(25):
        arrangement.blink()
        print('After', i+1, 'blinks the number of stones is:', arrangement.num_stones())
        # print(arrangement)


if __name__ == '__main__':
    main()
