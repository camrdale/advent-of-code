from collections import Counter
from collections import deque

from aoc.log import log, RESULT, INFO


def lanternfish(starting_fish: list[int], days: int) -> int:
    # Count the number of fish with each timer value.
    fish_counter: Counter[int] = Counter()
    fish_counter.update(starting_fish)

    # Queue of the counts of the number of fish with each timer value.
    # The leftmost items have a timer of zero, the next 1, etc.
    # The rightmost items have a timer of 6.
    existing_fish: deque[int] = deque()
    # Queue of the counts of the number of *new* fish with each timer value.
    # The leftmost items have a timer of 7, the next have a timer of 8.
    new_fish: deque[int] = deque()

    # First 7 (timers of 0-6) go in the existing_fish queue.
    for i in range(7):
        existing_fish.append(fish_counter[i])
    # Timers of 7 and 8 go in the new_fish queue.
    for i in range(7, 9):
        new_fish.append(fish_counter[i])
    
    for day in range(days):
        # Remove the counts for fish with timer 0 and 7 from the queues.
        # This has the side-effect of promoting all the other counts 
        multipliers = existing_fish.popleft()
        graduators = new_fish.popleft()
        # Each fish with timer 0 spawns that many new fish (timer 8)
        new_fish.append(multipliers)
        # Also add them to the back of the queue (timer 6) along with the
        # ones that graduated from the new_fish queue (were timer 7).
        existing_fish.append(graduators + multipliers)
        log(INFO, f'After day {day}, state is: {list(existing_fish) + list(new_fish)}')

    result = sum(existing_fish) + sum(new_fish)
    if len(str(result)) < 100:
        log(RESULT, days, 'days, total number of fish:', result)
    else:
        log(RESULT, days, 'days, number of digits in total number of fish:', len(str(result)))
    return result
