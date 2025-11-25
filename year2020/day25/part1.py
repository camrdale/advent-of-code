from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


SUBJECT = 7
MODULUS = 20201227


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        card_public = int(input[0])
        device_public = int(input[1])

        min_loop = 0
        value = 1
        i = 0
        while True:
            i += 1
            value = (value * SUBJECT) % MODULUS
            if value == card_public:
                min_loop = i
                subject = device_public
                break
            if value == device_public:
                min_loop = i
                subject = card_public
                break

        encryption_key = pow(subject, min_loop, MODULUS)

        log.log(log.RESULT, f'The encryption key: {encryption_key}')
        return encryption_key


part = Part1()

part.add_result(14897079, """
5764801
17807724
""")

part.add_result(8740494)
