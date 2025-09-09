from collections import deque
import re


GAME = re.compile(r'([0-9]*) players; last marble is worth ([0-9]*) points')


def play_game(num_players: int, num_points: int) -> int:
    marbles = deque([0])
    scores = {i: 0 for i in range(num_players)}

    for value in range(1, num_points + 1):
        if value % 23 == 0:
            marbles.rotate(7)
            scores[value % num_players] += value + marbles.popleft()
        else:
            marbles.rotate(-2)
            marbles.appendleft(value)

    return max(scores.values())
