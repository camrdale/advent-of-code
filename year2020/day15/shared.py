
def memory_game(starting_numbers: list[int], N: int) -> int:
    numbers = [0] * N

    n = 1
    for number in starting_numbers[:-1]:
        numbers[number] = n
        n += 1

    last_number = starting_numbers[-1]

    while n < N:
        last_occurrence = numbers[last_number]
        if last_occurrence != 0:
            new_number = n - last_occurrence
        else:
            new_number = 0
        numbers[last_number] = n
        last_number = new_number
        n += 1

    return last_number
