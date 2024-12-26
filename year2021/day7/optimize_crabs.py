#!/usr/bin/env python3

import sys

def part_two(filename):
  inputfile = open(filename, 'r')
  line = inputfile.readline()
  positions = [int(i) for i in line.strip().split(',')]
  
  min_sum = sys.maxsize
  min_position = 0

  for current_position in range(min(positions), max(positions) + 1):
    cheat = sum(
      abs(current_position - pos)*(abs(current_position - pos) + 1)/2
      for pos in positions)
    if cheat <= min_sum:
      min_sum = cheat
      min_position = current_position
    else:
      break

  print(filename, 'Min cost of', min_sum, 'found at position', min_position)


def part_one(filename):
  inputfile = open(filename, 'r')
  line = inputfile.readline()
  positions = [int(i) for i in line.strip().split(',')]
  positions.sort()
  
  print('Number of crabs:', len(positions))
  print('Leftmost position:', positions[0])
  print('Rightmost position:', positions[-1])

  left_positions_num = 0
  left_positions_sum = 0
  right_positions_num = len(positions)
  right_positions_sum = sum(positions)
  current_position = 0
  current_position_num = 0
  min_sum = left_positions_sum + right_positions_sum
  min_position = 0

  new_position = positions[0]
  while positions:
    left_positions_sum += left_positions_num * (new_position - current_position)
    left_positions_num += current_position_num
    left_positions_sum += current_position_num * (new_position - current_position)

    current_position_num = 0
    while positions and positions[0] == new_position:
      positions.pop(0)
      current_position_num += 1
      right_positions_num -= 1
      right_positions_sum -= (new_position - current_position)

    right_positions_sum -= right_positions_num * (new_position - current_position)
    current_position = new_position
    if left_positions_sum + right_positions_sum <= min_sum:
      min_sum = left_positions_sum + right_positions_sum
      min_position = current_position
    else:
      break

    #print('Curent Position:', current_position, left_positions_sum + right_positions_sum,
    #  'Left:', left_positions_num, left_positions_sum,
    #  'Current:', current_position_num,
    #  'Right:', right_positions_num, right_positions_sum) #, positions)
    new_position += 1

  print(filename, 'Min cost of', min_sum, 'found at position', min_position)

if __name__ == '__main__':
  part_one('example_input.txt')
  part_one('input.txt')
  part_two('example_input.txt')
  part_two('input.txt')
