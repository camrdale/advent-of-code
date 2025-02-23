import math
import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

CUT = re.compile(r'cut ([0-9-]*)')
DEAL_NEW_STACK = re.compile(r'deal into new stack')
DEAL_WITH_INCREMENT = re.compile(r'deal with increment ([0-9]*)')

N = 119315717514047
M = 101741582076661


def geometric_series(a: int, n : int, m : int) -> int:
    """Sum of geometric series modulo m, using repeated squaring.
    
    The geometric series is: 1 + a + a^2 + ... + a^n
    """
    sum = 0
    factor = 1
    while n > 0 and a != 0:
        if n % 2 == 0:
            temp = (factor * pow(a, n, m)) % m
            sum = (sum + temp) % m
            n -= 1
        factor = (((1 + a) % m) * factor) % m
        a = (a*a) % m
        n = math.floor(n / 2)
    return (sum + factor) % m


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        # y = m*x + b  (x = starting position, y = ending position)
        m = 1
        b = 0
        for line in input:
            if match := DEAL_NEW_STACK.match(line):
                m = (-m) % N
                b = (-b - 1) % N
            elif match := CUT.match(line):
                cut = int(match.group(1))
                b = (b - cut) % N
            elif match := DEAL_WITH_INCREMENT.match(line):
                increment = int(match.group(1))
                m = (m * increment) % N
                b = (b * increment) % N
            else:
                raise ValueError(f'Unparseable line: {line}')

        # Calculate the modular multiplicative inverse for going back one shuffle from y to get x
        # x = invmod(m, N) * (y - b) = i * (y - b)
        y = 2020
        invmod = pow(m, -1, N)
        log.log(log.INFO, f'inverse mod (m, N) = {invmod},  {invmod} x {m} % {N} = {(invmod*m) % N}')

        # Going back M shuffles requires
        # x = (i ^ M) * y - (i * b) * sum(1 + i + i^2 + ... + i^(M-1)) = mm * y + bm
        mm = pow(invmod, M, N)
        bm = (-invmod * b * geometric_series(invmod, M-1, N)) % N
        x = (mm * y + bm) % N
        log.log(log.INFO, f'Starting position = {x} = ({mm}*{y} + {bm}) % {N}')

        log.log(log.RESULT, f'Card that ends up in position 2020: {x}')
        return x


part = Part2()

part.add_result(37889219674304)
