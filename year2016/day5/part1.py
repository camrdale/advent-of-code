import hashlib

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()
        prefix = input[0].encode()

        prefix_hash = hashlib.md5(prefix)

        password = ''
        i = -1
        while len(password) < 8:
            while True:
                i += 1
                hash = prefix_hash.copy()
                hash.update(f'{i}'.encode())
                if hash.hexdigest().startswith('00000'):
                    break
            char = hash.hexdigest()[5]
            password += char
            log.log(log.INFO, f'Found character "{char}" from MD5 hash of "{input[0]}{i}": {hash.hexdigest()}')
    
        log.log(log.RESULT, f'Password for Door ID "{input[0]}": {password}')
        return password


part = Part1()

part.add_result('18f47a30', """
abc
""")

part.add_result('d4cd2ee1', """
ugkcyxxp
""")
