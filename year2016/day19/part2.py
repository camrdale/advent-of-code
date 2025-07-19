import math

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


# 178 sec
def secret_santa_winner(num_elves: int) -> int:
    l = list(range(num_elves))
    i = 0
    while len(l) > 1:
        steal_from = (i + (len(l) // 2)) % len(l)
        del l[steal_from]
        if steal_from > i:
            i = i + 1
        if i >= len(l):
            i = 0
    return l[0] + 1


class Elf:
    def __init__(self, num: int, next: 'Elf | None'):
        self.num = num
        self.next: Elf = next if next is not None else self


class LinkedList:
    def __init__(self):
        self.head: Elf | None = None
        self.tail: Elf | None = None
        self.length = 0

    def append(self, num: int):
        new_node = Elf(num, self.head)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.length += 1
            return
        assert self.tail is not None
        self.tail.next = new_node
        self.tail = new_node
        self.length += 1

    def delete(self, after_elf: Elf):
        after_elf.next = after_elf.next.next
        self.length -= 1


# 1.4 sec
def secret_santa_winner2(num_elves: int) -> int:
    l = LinkedList()
    to_delete = num_elves // 2
    delete_after: Elf | None = None
    for i in range(num_elves):
        l.append(i)
        if i == to_delete - 1:
            delete_after = l.tail
    assert delete_after is not None

    while l.length > 1:
        l.delete(delete_after)
        if l.length % 2 == 0:
            delete_after = delete_after.next

    return delete_after.num + 1


# 0 sec
def secret_santa_winner3(num_elves: int) -> int:
    power_of_3 = 3 ** math.floor(math.log(num_elves, 3))
    remaining = num_elves - power_of_3
    if remaining == 0:
        return power_of_3
    if remaining <= power_of_3:
        return remaining
    return power_of_3 + (remaining - power_of_3) * 2


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        num_elves = int(parser.get_input()[0])

        # for i in range(1, 100):
        #     log.log(log.INFO, f'{i}: {secret_santa_winner(i)}')
        # return -1

        winner = secret_santa_winner3(num_elves)

        log.log(log.RESULT, f'The elf that gets all the presents: {winner}')
        return winner


part = Part2()

part.add_result(2, """
5
""")

part.add_result(1410967, """
3005290
""")
