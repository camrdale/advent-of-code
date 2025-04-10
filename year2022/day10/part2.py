from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


class Part1(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()

        cycle = 0
        x = 1
        output = ""
        for line in input:
            operation = line.split()[0]
            cycles = 2 if operation == 'addx' else 1
            for _ in range(cycles):
                output += '\u2588' if x-1 <= cycle % 40 <= x+1 else ' '
                cycle += 1
                if cycle % 40 == 0:
                    output += '\n'
            if operation == 'addx':
                x += int(line.split()[1])

        log.log(log.RESULT, f'The image produced by the CRT:\n{output}')
        return output


part = Part1()

part.add_result("""██  ██  ██  ██  ██  ██  ██  ██  ██  ██  
███   ███   ███   ███   ███   ███   ███ 
████    ████    ████    ████    ████    
█████     █████     █████     █████     
██████      ██████      ██████      ████
███████       ███████       ███████     
""", r"""
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
""")

part.add_result("""███  █    ███   ██  ████ ███   ██  █    
█  █ █    █  █ █  █ █    █  █ █  █ █    
█  █ █    █  █ █  █ ███  ███  █    █    
███  █    ███  ████ █    █  █ █    █    
█    █    █    █  █ █    █  █ █  █ █    
█    ████ █    █  █ █    ███   ██  ████ 
""")
