#!/usr/bin/env python3

from collections import Counter

# Reference mapping of segment sets to corresponding numbers.
REFERENCE = {
  frozenset('acedgfb'): '8', frozenset('cdfbe'): '5', frozenset('gcdfa'): '2', frozenset('fbcad'): '3', 
  frozenset('dab'): '7', frozenset('cefabd'): '9', frozenset('cdfgeb'): '6', frozenset('eafb'): '4',
  frozenset('cagedb'): '0', frozenset('ab'): '1'}
# Count of the occurrences of each segment character in the patterns.
REFERENCE_SEGMENTS = Counter([c for word in REFERENCE for c in word])
# Scores (sum of the total counts of the occurrences of the segments)
# for the reference segment sets, mapped to their numbers.
REFERENCE_SCORES = dict(
  (sum(REFERENCE_SEGMENTS[c] for c in word), REFERENCE[word])
  for word in REFERENCE)

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

    # Count of the occurrences of each segment character in the patterns.
    segments = Counter([c for word in patterns for c in word])

    # Calculate the score for each pattern, and map that to the corresponding number
    # using the reference scores.
    mapping = dict(
      (word, REFERENCE_SCORES[sum(segments[c] for c in word)])
      for word in patterns)

    output_sum += int(''.join([mapping[word] for word in output]))

  print(filename, 'total number of 1/4/7/8:', lengths[2] + lengths[4] + lengths[3] + lengths[7])
  print(filename, 'total sum of output:', output_sum)


if __name__ == '__main__':
  main('example_input.txt')
  main('input.txt')
