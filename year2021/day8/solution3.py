#!/usr/bin/env python3

import itertools

from collections import Counter

# Reference mapping of segment sets to corresponding numbers.
REFERENCE = {
  frozenset('acedgfb'): '8', frozenset('cdfbe'): '5', frozenset('gcdfa'): '2', frozenset('fbcad'): '3', 
  frozenset('dab'): '7', frozenset('cefabd'): '9', frozenset('cdfgeb'): '6', frozenset('eafb'): '4',
  frozenset('cagedb'): '0', frozenset('ab'): '1'}
# A set of all the 10 segment sets.
REFERENCE_SET = set(REFERENCE.keys())
# A randomly chosen ordering to represent the segments.
REFERENCE_SEGMENTS = 'acedgfb'


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

    # Try all possible permutations of the 7 segments.
    for possibility in itertools.permutations(REFERENCE_SEGMENTS):
      # Create a mapping from the permutation to the reference segment.
      mapping = dict(zip(possibility, REFERENCE_SEGMENTS))
      # Use the mapping to try to convert the patterns to the reference segment sets.
      mapped_patterns = set(frozenset(mapping[c] for c in pattern) for pattern in patterns)
      # If the resutl is the reference, then the mapping works.
      if mapped_patterns == REFERENCE_SET:
        # Use the mapping to convert the outputs to the reference, then to the digits they represent.
        output_sum += int(''.join(REFERENCE[frozenset(mapping[c] for c in word)] for word in output))
        break

  print(filename, 'total number of 1/4/7/8:', lengths[2] + lengths[4] + lengths[3] + lengths[7])
  print(filename, 'total sum of output:', output_sum)


if __name__ == '__main__':
  main('example_input.txt')
  main('input.txt')
