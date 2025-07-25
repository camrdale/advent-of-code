from abc import ABC, abstractmethod


class Operation(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def apply(self, registers: dict[str, int]) -> int:
        """Apply the operation to the given registers. Return value is the offset to the next instruction."""
        pass

    def get_value(self, value: str, registers: dict[str, int]) -> int:
        try:
            return int(value)
        except ValueError:
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
    def __init__(self, value: str, register_or_offset: str) -> None:
        super().__init__()
        self.value = value
        self.register_or_offset = register_or_offset

    def apply(self, registers: dict[str, int]) -> int:
        if self.get_value(self.value, registers) != 0:
            return self.get_value(self.register_or_offset, registers)
        return 1


class OUT(Operation):
    def __init__(self, register: str, output: list[int]) -> None:
        super().__init__()
        self.register = register
        self.output = output

    def apply(self, registers: dict[str, int]) -> int:
        self.output.append(registers[self.register])
        return 1


class Computer:
    def __init__(self, instructions: list[str]) -> None:
        self.output: list[int] = []
        self.instructions: list[Operation] = []
        for instruction_input in instructions:
            match instruction_input.split():
                case ('cpy', value, register):
                    self.instructions.append(CPY(value, register))
                case ('inc', register):
                    self.instructions.append(INC(register))
                case ('dec', register):
                    self.instructions.append(DEC(register))
                case ('jnz', value, register_or_offset):
                    self.instructions.append(JNZ(value, register_or_offset))
                case ('out', register):
                    self.instructions.append(OUT(register, self.output))
                case _:
                    raise ValueError(f'Failed to parse instruction: {instruction_input}')

    def run(self, a: int = 0) -> dict[str, int]:
        registers = {'a': a, 'b': 0, 'c': 0, 'd': 0}
        self.output.clear()
        instruction = 0
        while instruction < len(self.instructions):
            instruction += self.instructions[instruction].apply(registers)
        return registers
