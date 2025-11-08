from abc import ABC, abstractmethod


class Operation(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def apply(self, registers: dict[str, int]) -> int:
        """Apply the operation to the given registers. Return value is the offset to the next instruction."""
        pass


class ACC(Operation):
    def __init__(self, amount: int) -> None:
        super().__init__()
        self.amount = amount

    def apply(self, registers: dict[str, int]) -> int:
        registers['accumulator'] += self.amount
        return 1


class JMP(Operation):
    def __init__(self, offset: int) -> None:
        super().__init__()
        self.offset = offset

    def apply(self, registers: dict[str, int]) -> int:
        return self.offset


class NOP(Operation):
    def __init__(self, offset: int) -> None:
        super().__init__()
        self.offset = offset

    def apply(self, registers: dict[str, int]) -> int:
        return 1


class Computer:
    def __init__(self, instructions: list[str]) -> None:
        self.instructions: list[Operation] = []
        for instruction_input in instructions:
            match instruction_input.split():
                case ('acc', amount):
                    self.instructions.append(ACC(int(amount)))
                case ('jmp', offset):
                    self.instructions.append(JMP(int(offset)))
                case ('nop', offset):
                    self.instructions.append(NOP(int(offset)))
                case _:
                    raise ValueError(f'Failed to parse instruction: {instruction_input}')

    def run(self) -> tuple[bool, dict[str, int]]:
        registers = {'accumulator': 0}
        instruction = 0
        executed: set[int] = set()
        while instruction < len(self.instructions):
            if instruction in executed:
                return False, registers
            executed.add(instruction)
            instruction += self.instructions[instruction].apply(registers)
        return True, registers
