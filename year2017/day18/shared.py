from abc import ABC, abstractmethod
import collections
import queue
import threading

from aoc import log


class State:
    def __init__(self, instructions: list[Operation], program_id: int, input: queue.SimpleQueue[int], output: queue.SimpleQueue[int], blocked: threading.Event) -> None:
        self.instruction = 0
        self.registers: dict[str, int] = collections.defaultdict(int)
        self.registers['p'] = program_id
        self.instructions = instructions
        self.input = input
        self.output = output
        self.blocked = blocked
        self.num_sends = 0
        self.program_id = program_id
        
    def __repr__(self) -> str:
        return f'State({self.instruction}, {self.registers}, {self.input.qsize()}, {self.output.qsize()})'


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


class ADD(Operation):
    def __init__(self, register: str, value: str) -> None:
        super().__init__()
        self.register = register
        self.value = value

    def apply(self, state: State) -> None:
        state.registers[self.register] += self.get_value(self.value, state.registers)
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
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.register}, {self.value})'


class MOD(Operation):
    def __init__(self, register: str, value: str) -> None:
        super().__init__()
        self.register = register
        self.value = value

    def apply(self, state: State) -> None:
        state.registers[self.register] %= self.get_value(self.value, state.registers)
        state.instruction += 1
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.register}, {self.value})'


class JGZ(Operation):
    def __init__(self, value: str, register_or_offset: str) -> None:
        super().__init__()
        self.value = value
        self.register_or_offset = register_or_offset

    def apply(self, state: State) -> None:
        if self.get_value(self.value, state.registers) > 0:
            state.instruction += self.get_value(self.register_or_offset, state.registers)
        else:
            state.instruction += 1
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.value}, {self.register_or_offset})'


class SND(Operation):
    def __init__(self, register: str) -> None:
        super().__init__()
        self.register = register

    def apply(self, state: State) -> None:
        state.output.put(state.registers[self.register])
        state.instruction += 1
        state.num_sends += 1
        log.log(log.INFO, f'Program {state.program_id} has sent: {state.num_sends}')
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.register})'


class RcvOccurred(Exception):
    def __init__(self, value: int, *args: object) -> None:
        super().__init__(*args)
        self.value = value


class RCVpart1(Operation):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def apply(self, state: State) -> None:
        state.instruction += 1
        if self.get_value(self.value, state.registers) != 0:
            last_sound = -1
            while True:
                try:
                    last_sound = state.input.get_nowait()
                except queue.Empty:
                    raise RcvOccurred(last_sound)
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.value})'


class RCVpart2(Operation):
    def __init__(self, register: str) -> None:
        super().__init__()
        self.register = register

    def apply(self, state: State) -> None:
        state.blocked.set()
        state.registers[self.register] = state.input.get()
        state.blocked.clear()
        state.instruction += 1
    
    def __repr__(self) -> str:
        return f'{super().__repr__()}({self.register})'


class Computer(threading.Thread):
    def __init__(self, instructions: list[str], program_id: int, input: queue.SimpleQueue[int], output: queue.SimpleQueue[int], blocked: threading.Event, part1: bool = True) -> None:
        super().__init__(daemon=True)
        self.program_id = program_id
        self.input = input
        self.output = output
        self.blocked = blocked
        self.instructions: list[Operation] = []
        for instruction_input in instructions:
            match instruction_input.split():
                case ('set', register, value):
                    self.instructions.append(SET(register, value))
                case ('add', register, value):
                    self.instructions.append(ADD(register, value))
                case ('mul', register, value):
                    self.instructions.append(MUL(register, value))
                case ('mod', register, value):
                    self.instructions.append(MOD(register, value))
                case ('jgz', value, register_or_offset):
                    self.instructions.append(JGZ(value, register_or_offset))
                case ('snd', register):
                    self.instructions.append(SND(register))
                case ('rcv', register):
                    if part1:
                        self.instructions.append(RCVpart1(register))
                    else:
                        self.instructions.append(RCVpart2(register))
                case _:
                    raise ValueError(f'Failed to parse instruction: {instruction_input}')
        self.state = State(self.instructions, self.program_id, self.input, self.output, self.blocked)

    def run(self) -> None:
        log.log(log.INFO, f'Program {self.program_id} started')
        while 0 <= self.state.instruction < len(self.state.instructions):
            log.log(log.INFO, f'BEFORE {self.program_id}: {self.state}, {self.state.instructions[self.state.instruction]}')
            self.state.instructions[self.state.instruction].apply(self.state)
        log.log(log.INFO, f'Program {self.program_id} finished')
