#!/usr/bin/env python3

from collections import Counter

def main(filename):
  inputfile = open(filename, 'r')
  # Count of the occurrences of each length of output value character.
  lengths = Counter()
  output_sum = 0

  while True:
    line = inputfile.readline()
    if not line:
      break
    
    words = [frozenset(word) for word in line.strip().split(' ')]
    patterns = words[0:10]
    output = words[11:15]
    lengths.update(len(s) for s in output)

    # Mapping of digits to the set of segments that make them.
    mapping = {}
    # Mapping of the set of segments to the digit they make.
    reverse_mapping = {}

    # Initialize with the obvious ones based on length.
    for word in patterns:
      if len(word) == 2:
        mapping[1] = word
        reverse_mapping[word] = 1
      if len(word) == 4:
        mapping[4] = word
        reverse_mapping[word] = 4
      if len(word) == 3:
        mapping[7] = word
        reverse_mapping[word] = 7
      if len(word) == 7:
        mapping[8] = word
        reverse_mapping[word] = 8

    # Union of 4 and 7 can only be a subset of 8 or 9.
    four_plus_seven = mapping[4].union(mapping[7])
    for word in patterns:
      if word == mapping[8]:
        continue
      if four_plus_seven <= word:
        reverse_mapping[word] = 9
        mapping[9] = word

    # Remaining 6 length digits 0 and 6, 1 is a subset of 0 but not 6.
    for word in patterns:
      if len(word) == 6 and word != mapping[9]:
        if mapping[1] <= word:
          reverse_mapping[word] = 0
          mapping[0] = word
        else:
          reverse_mapping[word] = 6
          mapping[6] = word

    # Of 5 length digits (2,3,5), only 5 unioned with 7 gives 9.
    for word in patterns:
      if len(word) == 5:
        if word.union(mapping[7]) == mapping[9]:
          reverse_mapping[word] = 5
          mapping[5] = word

    # Remaining 5 length digits 2 and 3, only 3 unioned with 5 gives 9.
    for word in patterns:
      if len(word) == 5 and word != mapping[5]:
        if word.union(mapping[5]) == mapping[9]:
          reverse_mapping[word] = 3
          mapping[3] = word
        else:
          reverse_mapping[word] = 2
          mapping[2] = word

    output_sum += int(''.join([str(reverse_mapping[word]) for word in output]))

  print(filename, 'total number of 1/4/7/8:', lengths[2] + lengths[4] + lengths[3] + lengths[7])
  print(filename, 'total sum of output:', output_sum)


if __name__ == '__main__':
  main('example_input.txt')
  main('input.txt')
