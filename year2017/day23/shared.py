from abc import ABC, abstractmethod
import collections
import string

from aoc import log


class State:
    def __init__(self, instructions: list[Operation]) -> None:
        self.instruction = 0
        self.registers: dict[str, int] = collections.defaultdict(int)
        self.instructions = instructions
        self.num_mul = 0
        
    def __repr__(self) -> str:
        return f'State({self.instruction}, {self.registers})'


class Operation(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def apply(self, state: State) -> None:
        """Apply the operation to the current state."""
        pass

    def get_value(self, value: str, registers: dict[str, int]) -> int:
        try:
            return int(value)
        except ValueError:
            return registers[value]
        
    def __repr__(self) -> str:
        return self.__class__.__name__


class SET(Operation):
    def __init__(self, register: str, value: str) -> None:
        super().__init__()
        self.register = register
        self.value = value

    def apply(self, state: State) -> None:
        state.registers[self.register] = self.get_value(self.value, state.registers)
        state.instruction += 1
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.register}, {self.value})'


class SUB(Operation):
    def __init__(self, register: str, value: str) -> None:
        super().__init__()
        self.register = register
        self.value = value

    def apply(self, state: State) -> None:
        state.registers[self.register] -= self.get_value(self.value, state.registers)
        state.instruction += 1
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.register}, {self.value})'


class MUL(Operation):
    def __init__(self, register: str, value: str) -> None:
        super().__init__()
        self.register = register
        self.value = value

    def apply(self, state: State) -> None:
        state.registers[self.register] *= self.get_value(self.value, state.registers)
        state.instruction += 1
        state.num_mul += 1
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.register}, {self.value})'


class JNZ(Operation):
    def __init__(self, value: str, register_or_offset: str) -> None:
        super().__init__()
        self.value = value
        self.register_or_offset = register_or_offset

    def apply(self, state: State) -> None:
        if self.get_value(self.value, state.registers) != 0:
            state.instruction += self.get_value(self.register_or_offset, state.registers)
        else:
            state.instruction += 1
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.value}, {self.register_or_offset})'


class Computer:
    def __init__(self, instructions: list[str]) -> None:
        self.instructions: list[Operation] = []
        for instruction_input in instructions:
            match instruction_input.split():
                case ('set', register, value):
                    self.instructions.append(SET(register, value))
                case ('sub', register, value):
                    self.instructions.append(SUB(register, value))
                case ('mul', register, value):
                    self.instructions.append(MUL(register, value))
                case ('jnz', value, register_or_offset):
                    self.instructions.append(JNZ(value, register_or_offset))
                case _:
                    raise ValueError(f'Failed to parse instruction: {instruction_input}')
        self.state = State(self.instructions)

    def run(self, debug: bool=False) -> None:
        if debug:
            print(f'{'Instruction':14}', ' '.join(f'{c:>8}' for c in string.ascii_lowercase[:8]))
        skip_steps = 0
        while 0 <= self.state.instruction < len(self.state.instructions):
            if debug:
                if skip_steps > 0:
                    skip_steps -= 1
                else:
                    steps = input(
                        f'{self.state.instructions[self.state.instruction]!r:15}'
                        + ' '.join(f'{self.state.registers[c]:8,}' for c in string.ascii_lowercase[:8])
                        + ' $ ')
                    if steps and steps.isdigit():
                        skip_steps = int(steps)

            if self.state.instruction == len(self.state.instructions) - 1:
                log.log(log.DEBUG,
                    f'{self.state.instructions[self.state.instruction]!r:15}'
                    + ' '.join(f'{self.state.registers[c]:8,}' for c in string.ascii_lowercase[:8]))

            self.state.instructions[self.state.instruction].apply(self.state)
