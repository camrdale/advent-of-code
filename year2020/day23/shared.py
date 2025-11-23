def play_cups(cups: list[int], starting_cup: int, num_moves: int):
    """cups is a linked list with the value at index i being the cup that follows cup i in the list."""
    max_target = len(cups) - 1
    current = starting_cup

    for _ in range(num_moves):
        pick_up_start = cups[current]
        pick_up_middle = cups[pick_up_start]
        pick_up_end = cups[pick_up_middle]
        
        target = current - 1 if current > 1 else max_target
        while target == pick_up_start or target == pick_up_middle or target == pick_up_end:
            target = target - 1 if target > 1 else max_target

        next = cups[pick_up_end]
        cups[pick_up_end] = cups[target]
        cups[target] = pick_up_start

        cups[current] = next
        current = next
