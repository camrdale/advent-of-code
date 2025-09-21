import math

from year2018.chronal import Computer


def sum_factors(n: int) -> int:
    step = 1
    if n % 2 == 1:
        step = 2

    total = 0
    for factor in range(1, int(math.sqrt(n)) + 1, step):
        if n % factor == 0:
            total += factor
            if factor != n // factor:
                total += n // factor
    
    return total


def run_optimized(computer: Computer, registers: dict[int, int]) -> None:
    # Run the start of the program (instructions 17-35), until it gets to the main loop.
    computer.run(registers, run_until_instruction=1)

    # The program finds the sum of the factors of a large number.
    # The value to find the factors of is in register 1.
    registers[0] = sum_factors(registers[1])
