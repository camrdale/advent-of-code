from abc import ABC, abstractmethod


class Operation(ABC):
    def __init__(self, a: int, b: int, c: int) -> None:
        self.a = a
        self.b = b
        self.c = c

    @abstractmethod
    def apply(self, registers: dict[int, int]) -> None:
        """Apply the operation to the current registers."""
        pass

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.a}, {self.b}, {self.c})'


class ADDR(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = registers[self.a] + registers[self.b]


class ADDI(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = registers[self.a] + self.b


class MULR(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = registers[self.a] * registers[self.b]


class MULI(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = registers[self.a] * self.b


class BANR(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = registers[self.a] & registers[self.b]


class BANI(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = registers[self.a] & self.b


class BORR(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = registers[self.a] | registers[self.b]


class BORI(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = registers[self.a] | self.b


class SETR(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = registers[self.a]


class SETI(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = self.a


class GTIR(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = 1 if self.a > registers[self.b] else 0


class GTRI(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = 1 if registers[self.a] > self.b else 0


class GTRR(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = 1 if registers[self.a] > registers[self.b] else 0


class EQIR(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = 1 if self.a == registers[self.b] else 0


class EQRI(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = 1 if registers[self.a] == self.b else 0


class EQRR(Operation):
    def apply(self, registers: dict[int, int]) -> None:
        registers[self.c] = 1 if registers[self.a] == registers[self.b] else 0


OPERATIONS: dict[str, type[Operation]] = {
    'addr': ADDR, 'addi': ADDI,
    'mulr': MULR, 'muli': MULI,
    'banr': BANR, 'bani': BANI,
    'borr': BORR, 'bori': BORI,
    'setr': SETR, 'seti': SETI,
    'gtir': GTIR, 'gtri': GTRI, 'gtrr': GTRR,
    'eqir': EQIR, 'eqri': EQRI, 'eqrr': EQRR}


class Computer:
    def __init__(self, input: list[str]) -> None:
        self.instructions: list[Operation] = []
        self.instruction_register: int | None = None
        for line in input:
            if line.startswith('#ip '):
                self.instruction_register = int(line.split()[1])
                continue
            op, a, b, c = line.split()
            self.instructions.append(OPERATIONS[op](int(a), int(b), int(c)))
        self.instruction = 0
        self.num_executed = 0

    def run(self, registers: dict[int, int], run_until_instruction: int | None = None, debug: bool=False) -> None:
        if debug:
            print(f'{'Instruction':19}', ' '.join(f'{i:>15}' for i in range(6)))
        skip_steps = 0
        while 0 <= self.instruction < len(self.instructions) and self.instruction != run_until_instruction:
            if self.instruction_register is not None:
                registers[self.instruction_register] = self.instruction

            if debug:
                if skip_steps > 0:
                    skip_steps -= 1
                else:
                    while True:
                        steps = input(
                            f'{self.instructions[self.instruction]!r:20}'
                            + ' '.join(f'{registers[i]:15,}' for i in range(6))
                            + ' $ ')
                        if not steps:
                            break
                        if steps.isdigit():
                            skip_steps = int(steps)
                            break
                        if steps.startswith('set '):
                            _, reg, val = steps.split()
                            registers[int(reg)] = int(val)

            self.instructions[self.instruction].apply(registers)
            self.num_executed += 1

            if self.instruction_register is not None:
                self.instruction = registers[self.instruction_register]
            self.instruction += 1
