#!/usr/bin/env python3

OPENING = {'(', '[', '{', '<'}
CLOSING_MAP = {')': '(', ']': '[', '}': '{', '>': '<'}
CLOSING_ERROR_SCORES = {')': 3, ']': 57, '}': 1197, '>': 25137}
COMPLETION_SCORES = {'(': 1, '[': 2, '{': 3, '<': 4}


def main(filename):
  inputfile = open(filename, 'r')
  syntax_score = 0
  autocompletion_scores = []

  while True:
    line = inputfile.readline()
    if not line:
      break
    
    chunks = list(line.strip())
    pending_opens = []
    for c in chunks:
      if c in OPENING:
        pending_opens.append(c)
        continue
      if not pending_opens or CLOSING_MAP[c] != pending_opens[-1]:
        syntax_score += CLOSING_ERROR_SCORES[c]
        break
      pending_opens.pop()
    else:
      # No break, so no errors found.
      pending_opens.reverse()
      score = 0
      for c in pending_opens:
        score *= 5
        score += COMPLETION_SCORES[c]
      autocompletion_scores.append(score)

  print(filename, 'total syntax error score is:', syntax_score)
  autocompletion_scores.sort()
  print(filename, 'middle autocompletion score is:',
    autocompletion_scores[int(len(autocompletion_scores) / 2)])


if __name__ == '__main__':
  main('example_input.txt')
  main('input.txt')
