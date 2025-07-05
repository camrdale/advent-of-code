import hashlib

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part2(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()
        estimated_iterations = parser.get_additional_params()[0]

        prefix = input[0].encode()
        prefix_hash = hashlib.md5(prefix)

        password = '________'
        i = -1
        chars_found = 0

        with log.ProgressBar(estimated_iterations=estimated_iterations, desc='day 5,2') as progress_bar:
            while chars_found < 8:
                while True:
                    i += 1
                    hash = prefix_hash.copy()
                    hash.update(f'{i}'.encode())
                    progress_bar.update()
                    if hash.hexdigest().startswith('00000'):
                        break
                position = hash.hexdigest()[5]
                char = hash.hexdigest()[6]
                if position.isdigit() and int(position) < 8:
                    if password[int(position)] != '_':
                        log.log(log.INFO, f'Ignoring duplicate character "{char}" for position {position} from MD5 hash of "{input[0]}{i}": {hash.hexdigest()}')
                        continue
                    password = password[:int(position)] + char + password[int(position)+1:]
                    chars_found += 1
                    log.log(log.INFO, f'Password is now "{password}", found character "{char}" from MD5 hash of "{input[0]}{i}": {hash.hexdigest()}')
    
        log.log(log.RESULT, f'Password for Door ID "{input[0]}": {password}')
        return password


part = Part2()

part.add_result('05ace8e3', """
abc
""", 13753421, include_progress=True)

part.add_result('f2c730e5', """
ugkcyxxp
""", 25176241)
