from abc import ABC, abstractmethod
import enum
import queue
import threading
from typing import overload

from aoc import log


class Memory:
    def __init__(self, initial_memory: list[int]):
        self.memory = list(initial_memory)
        self._relative_base: int = 0

    @property
    def relative_base(self) -> int:
        return self._relative_base

    @relative_base.setter
    def relative_base(self, offset: int) -> None:
        self._relative_base += offset

    def pad_memory(self, new_len: int) -> None:
        if new_len <= len(self.memory):
            return
        self.memory.extend([0]*(new_len - len(self.memory)))
        log.log(log.DEBUG, f'Memory padded to new length: {new_len}')

    @overload
    def __getitem__(self, index: int) -> int:
        pass

    @overload
    def __getitem__(self, index: slice) -> list[int]:
        pass

    def __getitem__(self, index: int | slice) -> int | list[int]:
        if isinstance(index, slice):
            self.pad_memory(index.stop)
        else:
            self.pad_memory(index + 1)
        return self.memory[index]

    def __setitem__(self, index: int, value: int):
        self.pad_memory(index + 1)
        self.memory[index] = value


class ParameterType(enum.Enum):
    INPUT = 1
    OUTPUT = 2


class Operation(ABC):
    parameter_types: tuple[ParameterType, ...] = ()
    short_name = 'NIL'

    def __init__(self, program_name: str, parameter_modes: list[int], input: queue.Queue[int], output: queue.Queue[int]):
        if len(parameter_modes) > len(self.parameter_types):
            raise ValueError(f'{program_name}: Operation {self} expected no more than {len(self.parameter_types)} parameter modes, got {parameter_modes}')
        self.program_name = program_name
        self.parameter_modes = parameter_modes
        self.input = input
        self.output = output
        self.raw_parameters: list[str] = []
        self.parsed_parameters: list[str] = []
        self.result: str = ''

    def get_parameters(self, parameters: tuple[int, ...], memory: Memory) -> list[int]:
        if len(parameters) != len(self.parameter_types):
            raise ValueError(f'{self.program_name}: Expected {self.parameter_types} parameters, got {parameters}')
        parsed_parameters: list[int] = []
        for i, parameter_type in enumerate(self.parameter_types):
            self.raw_parameters.append(f'{parameters[i]}')
            if i >= len(self.parameter_modes) or self.parameter_modes[i] == 0:
                # Position mode
                self.raw_parameters[-1] += 'p'
                if parameter_type == ParameterType.INPUT:
                    parsed_parameters.append(memory[parameters[i]])
                else:
                    parsed_parameters.append(parameters[i])
            elif self.parameter_modes[i] == 1:
                # Immediate mode
                self.raw_parameters[-1] += 'i'
                if parameter_type == ParameterType.INPUT:
                    parsed_parameters.append(parameters[i])
                else:
                    raise ValueError(f'{self.program_name}: Unexpected immediate parameter mode for output')
            elif self.parameter_modes[i] == 2:
                # Relative mode
                self.raw_parameters[-1] += 'r'
                if parameter_type == ParameterType.INPUT:
                    parsed_parameters.append(memory[memory.relative_base + parameters[i]])
                else:
                    parsed_parameters.append(memory.relative_base + parameters[i])
            else:
                raise ValueError(f'{self.program_name}: Unexpected parameter mode: {self.parameter_modes[i]}')
        self.parsed_parameters = list(map(str, parsed_parameters))
        return parsed_parameters

    @abstractmethod
    def apply(self, memory: Memory, *parameters: int) -> None | int:
        pass

    def __str__(self) -> str:
        s = [f'{self.short_name}({",".join(self.raw_parameters)})']
        s.append(f'{self.short_name}({",".join(self.parsed_parameters)})')
        if ParameterType.OUTPUT in self.parameter_types:
            i = self.parameter_types.index(ParameterType.OUTPUT)
            s.append(f'Memory[{self.parsed_parameters[i]}] = {self.result}')
        else:
            s.append(self.result)
        return ' -> '.join(s)


class Addition(Operation):
    parameter_types = (ParameterType.INPUT, ParameterType.INPUT, ParameterType.OUTPUT)
    short_name = 'ADD'

    def apply(self, memory: Memory, *parameters: int) -> None:
        input_parameter1, input_parameter2, output_location = self.get_parameters(parameters, memory)
        result = input_parameter1 + input_parameter2
        memory[output_location] = result
        self.result = str(result)


class Multiplication(Operation):
    parameter_types = (ParameterType.INPUT, ParameterType.INPUT, ParameterType.OUTPUT)
    short_name = 'MUL'
    
    def apply(self, memory: Memory, *parameters: int) -> None:
        input_parameter1, input_parameter2, output_location = self.get_parameters(parameters, memory)
        result = input_parameter1 * input_parameter2
        memory[output_location] = result
        self.result = str(result)


class Input(Operation):
    parameter_types = (ParameterType.OUTPUT,)
    short_name = 'IN'
    
    def apply(self, memory: Memory, *parameters: int) -> None:
        output_location, = self.get_parameters(parameters, memory)
        if self.input.empty():
            log.log(log.DEBUG, f'  {self.program_name}: Waiting on input')
        input_value = self.input.get()
        memory[output_location] = input_value
        self.result = str(input_value)


class Output(Operation):
    parameter_types = (ParameterType.INPUT,)
    short_name = 'OUT'
    
    def apply(self, memory: Memory, *parameters: int) -> None:
        input_parameter, = self.get_parameters(parameters, memory)
        self.output.put(input_parameter)
        self.result = f'Output {input_parameter}'


class LessThan(Operation):
    parameter_types = (ParameterType.INPUT, ParameterType.INPUT, ParameterType.OUTPUT)
    short_name = 'LT'

    def apply(self, memory: Memory, *parameters: int) -> None:
        input_parameter1, input_parameter2, output_location = self.get_parameters(parameters, memory)
        result = 1 if input_parameter1 < input_parameter2 else 0
        memory[output_location] = result
        self.result = str(result)


class Equals(Operation):
    parameter_types = (ParameterType.INPUT, ParameterType.INPUT, ParameterType.OUTPUT)
    short_name = 'EQ'

    def apply(self, memory: Memory, *parameters: int) -> None:
        input_parameter1, input_parameter2, output_location = self.get_parameters(parameters, memory)
        result = 1 if input_parameter1 == input_parameter2 else 0
        memory[output_location] = result
        self.result = str(result)


class JumpIfTrue(Operation):
    parameter_types = (ParameterType.INPUT, ParameterType.INPUT)
    short_name = 'JIT'

    def apply(self, memory: Memory, *parameters: int) -> int | None:
        input_parameter1, input_parameter2 = self.get_parameters(parameters, memory)
        if input_parameter1 != 0:
            self.result = f'JUMP {input_parameter2}'
            return input_parameter2
        self.result = 'NOOP'
        return None


class JumpIfFalse(Operation):
    parameter_types = (ParameterType.INPUT, ParameterType.INPUT)
    short_name = 'JIF'
    
    def apply(self, memory: Memory, *parameters: int) -> int | None:
        input_parameter1, input_parameter2 = self.get_parameters(parameters, memory)
        if input_parameter1 == 0:
            self.result = f'JUMP {input_parameter2}'
            return input_parameter2
        self.result = 'NOOP'
        return None


class RelativeBaseOffset(Operation):
    parameter_types = (ParameterType.INPUT,)
    short_name = 'RBO'
    
    def apply(self, memory: Memory, *parameters: int) -> None:
        input_parameter, = self.get_parameters(parameters, memory)
        memory.relative_base = input_parameter
        self.result = f'RelativeBase = {memory.relative_base}'


class Program(threading.Thread):
    OPERATIONS: dict[int, type[Operation]] = {
        1: Addition,
        2: Multiplication,
        3: Input,
        4: Output,
        5: JumpIfTrue,
        6: JumpIfFalse,
        7: LessThan,
        8: Equals,
        9: RelativeBaseOffset,
    }

    def __init__(self, name: str, memory: list[int]):
        super().__init__(name=name, daemon=True)
        self.memory = Memory(memory)

    def parse_instruction(self, instruction: int) -> tuple[int, list[int]]:
        opcode = instruction % 100
        parameter_modes: list[int] = []
        remaining_instruction = instruction // 100
        while remaining_instruction > 0:
            parameter_modes.append(remaining_instruction % 10)
            remaining_instruction = remaining_instruction // 10
        return opcode, parameter_modes

    def execute(self, input: queue.Queue[int], output: queue.Queue[int]) -> None:
        self.input = input
        self.output = output
        self.start()

    def run(self) -> None:
        log.log(log.INFO, f'{self.name}: is starting')
        instruction_pointer = 0
        num_instructions = 0
        while True:
            instruction = self.memory[instruction_pointer]
            num_instructions += 1
            opcode, parameter_modes = self.parse_instruction(instruction)
            if opcode == 99:
                break
            operation = self.OPERATIONS[opcode](self.name, parameter_modes, self.input, self.output)
            num_params = len(operation.parameter_types)
            parameters = self.memory[(instruction_pointer+1):(instruction_pointer+1+num_params)]
            next_instruction_pointer = operation.apply(self.memory, *parameters)
            log.log(log.DEBUG, f'  {self.name} {instruction:5d}: {operation}')
            if next_instruction_pointer is not None:
                instruction_pointer = next_instruction_pointer
            else:
                instruction_pointer += 1 + num_params
        log.log(log.INFO, f'{self.name}: is done, ran {num_instructions} instructions')
