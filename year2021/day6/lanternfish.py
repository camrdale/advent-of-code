#!/usr/bin/env python3

from collections import Counter
from collections import deque

def main(filename, days):
  inputfile = open(filename, 'r')
  line = inputfile.readline()
  starting_fish = [int(i) for i in line.strip().split(',')]

  # Count the number of fish with each timer value.
  fish_counter = Counter()
  fish_counter.update(starting_fish)

  # Queue of the counts of the number of fish with each timer value.
  # The leftmost items have a timer of zero, the next 1, etc.
  # The rightmost items have a timer of 6.
  existing_fish = deque()
  # Queue of the counts of the number of *new* fish with each timer value.
  # The leftmost items have a timer of 7, the next have a timer of 8.
  new_fish = deque()

  # First 7 (timers of 0-6) go in the existing_fish queue.
  for i in range(7):
    existing_fish.append(fish_counter[i])
  # Timers of 7 and 8 go in the new_fish queue.
  for i in range(7, 9):
    new_fish.append(fish_counter[i])
  
  for day in range(1, days + 1):
    # Remove the counts for fish with timer 0 and 7 from the queues.
    # This has the side-effect of promoting all the other counts 
    multipliers = existing_fish.popleft()
    graduators = new_fish.popleft()
    # Each fish with timer 0 spawns that many new fish (timer 8)
    new_fish.append(multipliers)
    # Also add them to the back of the queue (timer 6) along with the
    # ones that graduated from the new_fish queue (were timer 7).
    existing_fish.append(graduators + multipliers)
    # print('After day', day, 'state is:', list(existing_fish) + list(new_fish))

  result = str(sum(existing_fish) + sum(new_fish))
  if len(result) < 100:
    print(filename, days, 'days, total number of fish:', result)
  else:
    print(filename, days, 'days, number of digits in total number of fish:', len(result))


if __name__ == '__main__':
  main('example_input.txt', 80)
  main('input.txt', 80)
  main('example_input.txt', 256)
  main('input.txt', 256)
  main('example_input.txt', 9999999)
