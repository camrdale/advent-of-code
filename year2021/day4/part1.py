from aoc.input import InputParser
from aoc.log import log, RESULT, INFO, DEBUG
from aoc.runner import Part

# Possible lines to check on a 25 entry list representing a 5x5 card,
# in the form (starting offset, increment).
POSSIBILITIES = [
    # 5 rows
    (0, 1),
    (5, 1),
    (10, 1),
    (15, 1),
    (20, 1),
    # 5 columns
    (0, 5),
    (1, 5),
    (2, 5),
    (3, 5),
    (4, 5),
]


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        call_order = [int(i) for i in input[0].split(',')]
        # Map from the number called, to which turn it was called on (zero-based).
        call_turn = {call: turn for turn, call in enumerate(call_order)}

        # Skip the empty line
        line_num = 2

        min_first_bingo = 100
        min_bingo_card = []
        
        while line_num < len(input):
            card: list[int] = []
            for i in range(5):
                card_line = [int(i) for i in input[line_num + i].split()]
                if len(card_line) != 5:
                    print('ERROR: Unexpected card width:', input[line_num + i])
                    return -1
                card.extend(card_line)
            
            # Bingo card with the numbers replaced by the turn each number is called.
            card_with_turns = [call_turn[number] for number in card]

            # Find the max turn for each possible line in the card, that is when it would be a Bingo.
            # The min of those possible Bingos is the first Bingo for the card.
            first_bingo = min(
                max(card_with_turns[i] for i in range(start, start + 5*increment, increment))
                for (start, increment) in POSSIBILITIES)

            if first_bingo < min_first_bingo:
                min_first_bingo = first_bingo
                min_bingo_card = card_with_turns

            # Skip the empty line
            line_num += 6

        log(INFO, 'Found the first bingo at turn:', min_first_bingo)
        log(DEBUG, 'First bingo is in card:', [call_order[order] for order in min_bingo_card])
        unmarked_numbers = [call_order[order] for order in min_bingo_card if order > min_first_bingo]
        score = call_order[min_first_bingo] * sum(unmarked_numbers)
        log(RESULT, 'Score for first card to bingo is:', score)
        return score


part = Part1()

part.add_result(4512, """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
""")

part.add_result(22680)
