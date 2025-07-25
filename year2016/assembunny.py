from abc import ABC, abstractmethod

from aoc import log


class State:
    def __init__(self, instructions: list['Operation'], a: int = 0, c: int = 0) -> None:
        self.instruction = 0
        self.registers = {'a': a, 'b': 0, 'c': c, 'd': 0}
        self.instructions = instructions
        self.output: list[int] = []


class Operation(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def apply(self, state: State) -> None:
        """Apply the operation to the current state."""
        pass

    @abstractmethod
    def toggle(self) -> 'Operation':
        """Return the new operation that is this one toggled."""
        pass

    def get_value(self, value: str, registers: dict[str, int]) -> int:
        try:
            return int(value)
        except ValueError:
            return registers[value]
        
    def __repr__(self) -> str:
        return self.__class__.__name__


class NOOP(Operation):
    def __init__(self) -> None:
        super().__init__()

    def apply(self, state: State) -> None:
        state.instruction += 1
    
    def toggle(self) -> Operation:
        raise ValueError(f'Can not toggle a NOOP')
    

class CPY(Operation):
    def __init__(self, value: str, register: str) -> None:
        super().__init__()
        self.value = value
        self.register = register

    def apply(self, state: State) -> None:
        if self.register in state.registers:
            state.registers[self.register] = self.get_value(self.value, state.registers)
        state.instruction += 1
    
    def toggle(self) -> Operation:
        return JNZ(self.value, self.register)
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.value}, {self.register})'


class INC(Operation):
    def __init__(self, register: str) -> None:
        super().__init__()
        self.register = register

    def apply(self, state: State) -> None:
        state.registers[self.register] += 1
        state.instruction += 1
    
    def toggle(self) -> Operation:
        return DEC(self.register)
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.register})'


class DEC(Operation):
    def __init__(self, register: str) -> None:
        super().__init__()
        self.register = register

    def apply(self, state: State) -> None:
        state.registers[self.register] -= 1
        state.instruction += 1
    
    def toggle(self) -> Operation:
        return INC(self.register)
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.register})'


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
    
    def toggle(self) -> Operation:
        return CPY(self.value, self.register_or_offset)
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.value}, {self.register_or_offset})'


class TGL(Operation):
    def __init__(self, register: str) -> None:
        super().__init__()
        self.register = register

    def apply(self, state: State) -> None:
        toggle = state.instruction + state.registers[self.register]
        if 0 <= toggle < len(state.instructions):
            state.instructions[toggle] = state.instructions[toggle].toggle()
        state.instruction += 1
    
    def toggle(self) -> Operation:
        return INC(self.register)
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.register})'


class ADD(Operation):
    def __init__(self, value: str, register: str) -> None:
        super().__init__()
        self.value = value
        self.register = register

    def apply(self, state: State) -> None:
        if self.register in state.registers:
            state.registers[self.register] += self.get_value(self.value, state.registers)
        state.instruction += 1
    
    def toggle(self) -> Operation:
        raise ValueError(f'Can not toggle a ADD')
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.value}, {self.register})'


class MUL(Operation):
    def __init__(self, value1: str, value2: str, register: str) -> None:
        super().__init__()
        self.value1 = value1
        self.value2 = value2
        self.register = register

    def apply(self, state: State) -> None:
        state.registers[self.register] += self.get_value(self.value1, state.registers) * self.get_value(self.value2, state.registers)
        state.instruction += 1
    
    def toggle(self) -> Operation:
        raise ValueError(f'Can not toggle a MUL')
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.value1}, {self.value2}, {self.register})'


class OUT(Operation):
    def __init__(self, register: str) -> None:
        super().__init__()
        self.register = register

    def apply(self, state: State) -> None:
        state.output.append(state.registers[self.register])
        state.instruction += 1

    def toggle(self) -> Operation:
        raise ValueError(f'Can not toggle a OUT')
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.register})'


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
                case ('jnz', value, register_or_offset):
                    self.instructions.append(JNZ(value, register_or_offset))
                case ('tgl', register):
                    self.instructions.append(TGL(register))
                case ('out', register):
                    self.instructions.append(OUT(register))
                case _:
                    raise ValueError(f'Failed to parse instruction: {instruction_input}')
        self.optimize()

    def run(self, a: int = 0, c: int = 0) -> State:
        state = State(list(self.instructions), a=a, c=c)
        while state.instruction < len(state.instructions):
            state.instructions[state.instruction].apply(state)
        return state

    def optimize(self) -> None:
        # Replace INC/DEC/JNZ-2 with ADD - reduces time to run by 37.5%
        for i in range(len(self.instructions) - 1, 1, -1):
            instruction = self.instructions[i]
            instruction_1 = self.instructions[i-1]
            instruction_2 = self.instructions[i-2]
            if isinstance(instruction, JNZ) and instruction.register_or_offset == '-2':
                if isinstance(instruction_1, DEC) and instruction_1.register == instruction.value and isinstance(instruction_2, INC):
                    self.instructions[i-2] = NOOP()
                    self.instructions[i-1] = ADD(instruction_1.register, instruction_2.register)
                    self.instructions[i] = CPY('0', instruction_1.register)
                if isinstance(instruction_2, DEC) and instruction_2.register == instruction.value and isinstance(instruction_1, INC):
                    self.instructions[i-2] = NOOP()
                    self.instructions[i-1] = ADD(instruction_2.register, instruction_1.register)
                    self.instructions[i] = CPY('0', instruction_2.register)

        # Replace ADD/DEC/JNZ-5 with MUL - reduces time to run by 99.999%
        for i in range(len(self.instructions) - 1, 3, -1):
            instruction = self.instructions[i]
            instruction_1 = self.instructions[i-1]
            instruction_5 = self.instructions[i-5]
            if isinstance(instruction, JNZ) and instruction.register_or_offset == '-5' and isinstance(instruction_1, DEC) and instruction_1.register == instruction.value:
                assert isinstance(instruction_5, CPY)
                op1 = instruction_5.value
                op2 = instruction_1.register

                add_instructions = [j for j, inst in enumerate(self.instructions) if j > i-5 and j < i and isinstance(inst, ADD)]
                assert len(add_instructions) == 1, add_instructions
                add_instruction = self.instructions[add_instructions[0]]
                assert isinstance(add_instruction, ADD)
                dest = add_instruction.register
                self.instructions[add_instructions[0]] = NOOP()

                self.instructions[i-1] = MUL(op1, op2, dest)
                self.instructions[i] = CPY('0', instruction_1.register)
        
        log.log(log.DEBUG, 'Post-optimization instructions:')
        log.log(log.DEBUG, '\n'.join(str(inst) for inst in self.instructions))
