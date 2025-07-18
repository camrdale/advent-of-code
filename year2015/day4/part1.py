import hashlib

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        prefix = input[0].encode()

        prefix_hash = hashlib.md5(prefix)

        i = 0
        while True:
            hash = prefix_hash.copy()
            hash.update(f'{i}'.encode())
            if hash.hexdigest().startswith('00000'):
                break
            i += 1

        log.log(log.RESULT, f'MD5 hash of "{input[0]}{i}": {hash.hexdigest()}')
        return i


part = Part1()

part.add_result(609043, """
abcdef
""")

part.add_result(1048970, """
pqrstuv
""")

part.add_result(117946, """
ckczppom
""")
