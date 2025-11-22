from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from collections import deque


game = 1


def play_round(player1_cards: tuple[int, ...], player2_cards: tuple[int, ...]) -> tuple[bool, tuple[int, ...]]:
    global game
    this_game = game
    log.log(log.INFO, f'=== Game {this_game} ===')
    player1 = deque(player1_cards)
    player2 = deque(player2_cards)

    round = 0
    previous_rounds: set[int] = set()
    while len(player1) > 0 and len(player2) > 0:
        round += 1

        # Logging (even when disabled) is too slow.
        # log.log(log.DEBUG, )
        # log.log(log.DEBUG, f'-- Round {round} (Game {this_game}) -- ')
        # log.log(log.DEBUG, f'Player 1\'s deck: {", ".join(map(str, player1))}')
        # log.log(log.DEBUG, f'Player 2\'s deck: {", ".join(map(str, player2))}')

        new_round = hash(tuple(player1) + (0,) + tuple(player2))
        if new_round in previous_rounds:
            # log.log(log.DEBUG, 'Duplicate round:', player1, player2)
            return True, tuple(player1)
        previous_rounds.add(new_round)

        c1 = player1.popleft()
        c2 = player2.popleft()

        # log.log(log.DEBUG, f'Player 1 plays: {c1}')
        # log.log(log.DEBUG, f'Player 2 plays: {c2}')

        player1_winner = c1 > c2

        if c1 <= len(player1) and c2 <= len(player2):
            sub_player1 = tuple(player1)[:c1]
            sub_player2 = tuple(player2)[:c2]

            game += 1
            # log.log(log.DEBUG, f'Playing a sub-game to determine the winner...')
            # log.log(log.DEBUG, )

            player1_winner, _ = play_round(sub_player1, sub_player2)

            # log.log(log.DEBUG, )
            # log.log(log.DEBUG, f'...anyway, back to game {this_game}.')

        # log.log(log.DEBUG, f'Player {1 if player1_winner else 2} wins round {round} of game {this_game}!')

        if player1_winner:
            player1.append(c1)
            player1.append(c2)
        else:
            player2.append(c2)
            player2.append(c1)

    winner = len(player1) > 0
    log.log(log.INFO, f'The winner of game {this_game} is player {1 if winner else 2} after {round} rounds')
    return winner, tuple(player1 if winner else player2)


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        player1_input, player2_input = parser.get_two_part_input()

        player1 = tuple(map(int, player1_input[1:]))
        player2 = tuple(map(int, player2_input[1:]))
        global game
        game = 1

        winner, cards = play_round(player1, player2)

        log.log(log.INFO, )
        log.log(log.INFO, )
        log.log(log.INFO, '== Post-game results ==')
        log.log(log.INFO, f'Player 1\'s deck: {", ".join(map(str, cards if winner else []))}')
        log.log(log.INFO, f'Player 2\'s deck: {", ".join(map(str, cards if not winner else []))}')

        score = sum([
            card * (i + 1)
            for i, card in enumerate(cards[::-1])
        ])

        log.log(log.RESULT, f'Player {1 if winner else 2} wins with score: {score}')
        return score


part = Part2()

part.add_result(105, """
Player 1:
43
19

Player 2:
2
29
14
""")

part.add_result(291, """
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

part.add_result(35676)
