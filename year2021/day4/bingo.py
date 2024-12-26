#!/usr/bin/env python3

import sys

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

def main(filename):
  print('Parsing file:', filename)
  inputfile = open(filename, 'r')
  line = inputfile.readline()
  call_order = [int(i) for i in line.strip().split(',')]
  # Map from the number called, to which turn it was called on (zero-based).
  call_turn = {call: turn for turn, call in enumerate(call_order)}

  # Skip the empty line
  line = inputfile.readline()

  min_first_bingo = 100
  min_bingo_card = []
  max_first_bingo = 0
  max_bingo_card = []
  
  while True:
    card = []
    for _ in range(5):
      line = inputfile.readline()
      if not line:
        print('ERROR: Unexpected EOF found!', file=sys.stderr)
        exit(1)
      card_line = [int(i) for i in line.strip().split()]
      if len(card_line) != 5:
        print('ERROR: Unexpected card width:', line, file=sys.stderr)
        exit(2)
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
    if first_bingo > max_first_bingo:
      max_first_bingo = first_bingo
      max_bingo_card = card_with_turns

    # Skip the empty line
    line = inputfile.readline()
    if not line:
      break

  print('Found the first bingo at turn:', min_first_bingo)
  print('First bingo is in card:', [call_order[order] for order in min_bingo_card])
  unmarked_numbers = [call_order[order] for order in min_bingo_card if order > min_first_bingo]
  score = call_order[min_first_bingo] * sum(unmarked_numbers)
  print('Score is:', score)

  print('Found the last bingo at turn:', max_first_bingo)
  print('Last bingo is in card:', [call_order[order] for order in max_bingo_card])
  unmarked_numbers = [call_order[order] for order in max_bingo_card if order > max_first_bingo]
  score = call_order[max_first_bingo] * sum(unmarked_numbers)
  print('Score is:', score)

if __name__ == '__main__':
  main('example_input.txt')
  main('input.txt')
