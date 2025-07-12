from abc import ABC, abstractmethod


class Operation(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def apply(self, registers: dict[str, int]) -> int:
        """Apply the operation to the given registers. Return value is the offset to the next instruction."""
        pass

    def get_value(self, value: str, registers: dict[str, int]) -> int:
        if value.isdigit():
            return int(value)
        return registers[value]


class CPY(Operation):
    def __init__(self, value: str, register: str) -> None:
        super().__init__()
        self.value = value
        self.register = register

    def apply(self, registers: dict[str, int]) -> int:
        registers[self.register] = self.get_value(self.value, registers)
        return 1


class INC(Operation):
    def __init__(self, register: str) -> None:
        super().__init__()
        self.register = register

    def apply(self, registers: dict[str, int]) -> int:
        registers[self.register] += 1
        return 1


class DEC(Operation):
    def __init__(self, register: str) -> None:
        super().__init__()
        self.register = register

    def apply(self, registers: dict[str, int]) -> int:
        registers[self.register] -= 1
        return 1


class JNZ(Operation):
    def __init__(self, value: str, offset: int) -> None:
        super().__init__()
        self.value = value
        self.offset = offset

    def apply(self, registers: dict[str, int]) -> int:
        if self.get_value(self.value, registers) != 0:
            return self.offset
        return 1


class Computer:
    def __init__(self, instructions: list[str]) -> None:
        self.instructions: list[Operation] = []
        for instruction_input in instructions:
            match instruction_input.split():
                case ('cpy', value, register):
                    self.instructions.append(CPY(value, register))
                case ('inc', register):
                    self.instructions.append(INC(register))
                case ('dec', register):
                    self.instructions.append(DEC(register))
                case ('jnz', value, offset):
                    self.instructions.append(JNZ(value, int(offset)))
                case _:
                    raise ValueError(f'Failed to parse instruction: {instruction_input}')

    def run(self, c: int = 0) -> dict[str, int]:
        registers = {'a': 0, 'b': 0, 'c': c, 'd': 0}
        instruction = 0
        while instruction < len(self.instructions):
            instruction += self.instructions[instruction].apply(registers)
        return registers
