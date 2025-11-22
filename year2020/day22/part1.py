from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from collections import deque


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        player1_input, player2_input = parser.get_two_part_input()

        player1 = deque(map(int, player1_input[1:]))
        player2 = deque(map(int, player2_input[1:]))

        rounds = 0
        while len(player1) > 0 and len(player2) > 0:
            c1 = player1.popleft()
            c2 = player2.popleft()
            if c1 > c2:
                player1.append(c1)
                player1.append(c2)
            else:
                player2.append(c2)
                player2.append(c1)
            rounds += 1

        score = sum([
            card * (i + 1)
            for i, card in enumerate(list(player1 if len(player1) > 0 else player2)[::-1])
        ])        

        log.log(log.RESULT, f'After {rounds} rounds, player {1 if len(player1) > 0 else 2} wins with score: {score}')
        return score


part = Part1()

part.add_result(306, """
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
""")

part.add_result(32489)
