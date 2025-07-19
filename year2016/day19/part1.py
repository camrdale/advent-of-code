from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


# 69 msec
def secret_santa_winner(num_elves: int) -> int:
    l = list(range(num_elves))
    while len(l) > 1:
        n = len(l)
        del l[1::2]
        if n % 2 != 0:
            del l[0]
    return l[0] + 1


# 0 msec
def secret_santa_winner2(num_elves: int) -> int:
    n = num_elves
    offset = 0
    skip = 2
    while n > 1:
        if n % 2 != 0:
            n = n - 1
            offset = offset + skip
        n = n // 2
        skip = skip * 2

    return offset + 1


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        num_elves = int(parser.get_input()[0])

        winner = secret_santa_winner2(num_elves)

        log.log(log.RESULT, f'The elf that gets all the presents: {winner}')
        return winner


part = Part1()

part.add_result(3, """
5
""")

part.add_result(1816277, """
3005290
""")
