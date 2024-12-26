from aoc.input import InputParser
from aoc.log import log, RESULT, DEBUG
from aoc.runner import Part

from typing import NamedTuple, cast


class KeyOrLock(NamedTuple):
    columns: tuple[int, int, int, int, int]


class Key(KeyOrLock):
    pass


class Lock(KeyOrLock):
    pass

    def compatible(self, key: Key) -> bool:
        return (self.columns[0] + key.columns[0] <= 5 and
                self.columns[1] + key.columns[1] <= 5 and
                self.columns[2] + key.columns[2] <= 5 and
                self.columns[3] + key.columns[3] <= 5 and
                self.columns[4] + key.columns[4] <= 5)


class KeyCompatible:

    def __init__(self):
        self.compatibilities: list[list[set[Key]]] = []
        self.total_keys = 0
        for _ in range(5):
            heights: list[set[Key]] = []
            for _ in range(6):
                heights.append(set())
            self.compatibilities.append(heights)

    def add_key(self, key: Key) -> None:
        self.total_keys += 1
        for column in range(5):
            height = key.columns[column]
            # Don't keep a set for compatibility with height 0, it would just contain every key.
            for compatible_with in range(1, 6 - height):
                self.compatibilities[column][compatible_with].add(key)

    def num_compatible_with(self, lock: Lock) -> int:
        sets: list[set[Key]] = [
            self.compatibilities[column][height]
            for column, height in enumerate(lock.columns)
            if height > 0]
        if len(sets) == 0:
            # All heights are 0 for this lock, so it's compatible with everything.
            return self.total_keys
        return len(sets[0].intersection(*sets[1:]))


def parse(key_or_lock: type[KeyOrLock], lines: list[str]) -> KeyOrLock:
    columns: list[int] = [0, 0, 0, 0, 0]
    for line in lines:
        for i, c in enumerate(line):
            if c == '#':
                columns[i] += 1
    return key_or_lock(cast(tuple[int, int, int, int, int], tuple(columns)))


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        locks: list[Lock] = []
        keys: list[Key] = []
        i = 0
        while i < len(input):
            if input[i] == '#####':
                lock = cast(Lock, parse(Lock, input[i+1:i+6]))
                locks.append(lock)
            if input[i] == '.....':
                key = cast(Key, parse(Key, input[i+5:i:-1]))
                keys.append(key)
            i += 8

        log(DEBUG, f'Found {len(locks)} locks and {len(keys)} keys')

        for lock in locks:
            log(DEBUG, f'Lock {lock.columns}')
        for key in keys:
            log(DEBUG, f'Key  {key.columns}')

        key_compatible = KeyCompatible()
        
        for key in keys:
            key_compatible.add_key(key)
        
        compatible_keys_and_locks = 0
        for lock in locks:
            compatible_keys_and_locks += key_compatible.num_compatible_with(lock)

        log(RESULT, f'Number of compatible key and lock combinations: {compatible_keys_and_locks}')
        return compatible_keys_and_locks


part = Part1()

part.add_result(3, """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
""")

# Degenerate case with empty lock/key.
part.add_result(4, """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
.....
.....
.....
.....
.....
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
.....
.....
.....
#####
""")

# Degenerate case with one height lock/key.
part.add_result(4, """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
..#..
.....
.....
.....
.....
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
.....
.....
..#..
#####
""")

part.add_result(3269)
