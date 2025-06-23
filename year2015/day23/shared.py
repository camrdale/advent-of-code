from abc import ABC, abstractmethod


class Operation(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def apply(self, registers: dict[str, int]) -> int:
        """Apply the operation to the given registers. Return value is the offset to the next instruction."""
        pass


class HLF(Operation):
    def __init__(self, register: str) -> None:
        super().__init__()
        self.register = register

    def apply(self, registers: dict[str, int]) -> int:
        registers[self.register] //= 2
        return 1    


class TPL(Operation):
    def __init__(self, register: str) -> None:
        super().__init__()
        self.register = register

    def apply(self, registers: dict[str, int]) -> int:
        registers[self.register] *= 3
        return 1    


class INC(Operation):
    def __init__(self, register: str) -> None:
        super().__init__()
        self.register = register

    def apply(self, registers: dict[str, int]) -> int:
        registers[self.register] += 1
        return 1    


class JMP(Operation):
    def __init__(self, offset: int) -> None:
        super().__init__()
        self.offset = offset

    def apply(self, registers: dict[str, int]) -> int:
        return self.offset


class JIE(Operation):
    def __init__(self, register: str, offset: int) -> None:
        super().__init__()
        self.register = register
        self.offset = offset

    def apply(self, registers: dict[str, int]) -> int:
        if registers[self.register] % 2 == 0:
            return self.offset
        return 1


class JIO(Operation):
    def __init__(self, register: str, offset: int) -> None:
        super().__init__()
        self.register = register
        self.offset = offset

    def apply(self, registers: dict[str, int]) -> int:
        if registers[self.register] == 1:
            return self.offset
        return 1


class Computer:
    def __init__(self, instructions: list[str]) -> None:
        self.instructions: list[Operation] = []
        for instruction_input in instructions:
            match instruction_input.split():
                case ('hlf', register):
                    self.instructions.append(HLF(register))
                case ('tpl', register):
                    self.instructions.append(TPL(register))
                case ('inc', register):
                    self.instructions.append(INC(register))
                case ('jmp', offset):
                    self.instructions.append(JMP(int(offset)))
                case ('jie', register, offset):
                    self.instructions.append(JIE(register[0], int(offset)))
                case ('jio', register, offset):
                    self.instructions.append(JIO(register[0], int(offset)))
                case _:
                    raise ValueError(f'Failed to parse instruction: {instruction_input}')

    def run(self, a: int = 0) -> dict[str, int]:
        registers = {'a': a, 'b': 0}
        instruction = 0
        while instruction < len(self.instructions):
            instruction += self.instructions[instruction].apply(registers)
        return registers
