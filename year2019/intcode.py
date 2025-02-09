from abc import ABC, abstractmethod
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


class Operation(ABC):
    def __init__(self, program_name: str, parameter_modes: list[int], input: queue.Queue[int], output: queue.Queue[int]):
        if len(parameter_modes) > self.num_parameters():
            raise ValueError(f'{program_name}: Operation {self} expected no more than {self.num_parameters()} parameter modes, got {parameter_modes}')
        self.program_name = program_name
        self.parameter_modes = parameter_modes
        self.input = input
        self.output = output

    def parse_input_parameters(self, num_input_parameters: int, parameters: tuple[int, ...], memory: Memory) -> list[int]:
        if len(parameters) != self.num_parameters():
            raise ValueError(f'{self.program_name}: Expected {self.num_parameters()} parameters, got {parameters}')
        parsed_parameters: list[int] = []
        for i in range(num_input_parameters):
            if i >= len(self.parameter_modes) or self.parameter_modes[i] == 0:
                # Position mode
                parsed_parameters.append(memory[parameters[i]])
            elif self.parameter_modes[i] == 1:
                # Immediate mode
                parsed_parameters.append(parameters[i])
            elif self.parameter_modes[i] == 2:
                # Relative mode
                parsed_parameters.append(memory[memory.relative_base + parameters[i]])
            else:
                raise ValueError(f'{self.program_name}: Unexpected parameter mode: {self.parameter_modes[i]}')
        return parsed_parameters

    def parse_output_parameter(self, parameter_num: int, parameter: int, memory: Memory) -> int:
        if parameter_num >= len(self.parameter_modes) or self.parameter_modes[parameter_num] == 0:
            # Position mode
            return parameter
        elif self.parameter_modes[parameter_num] == 1:
            # Immediate mode
            raise ValueError(f'{self.program_name}: Unexpected immediate parameter mode for output')
        elif self.parameter_modes[parameter_num] == 2:
            # Relative mode
            return memory.relative_base + parameter
        else:
            raise ValueError(f'{self.program_name}: Unexpected parameter mode for output: {self.parameter_modes[parameter_num]}')

    @abstractmethod
    def num_parameters(self) -> int:
        pass

    @abstractmethod
    def apply(self, memory: Memory, *parameters: int) -> None | int:
        pass


class Addition(Operation):


    def num_parameters(self) -> int:
        return 3
    
    def apply(self, memory: Memory, *parameters: int) -> None:
        input_parameter1, input_parameter2 = self.parse_input_parameters(2, parameters, memory)
        result = input_parameter1 + input_parameter2
        memory[self.parse_output_parameter(2, parameters[2], memory)] = result
        log.log(log.DEBUG, f'  {self.program_name}: Addition on {parameters[0]} ({input_parameter1}) and {parameters[1]} ({input_parameter2}) stored in {parameters[2]} ({result})')


class Multiplication(Operation):
    def num_parameters(self) -> int:
        return 3
    
    def apply(self, memory: Memory, *parameters: int) -> None:
        input_parameter1, input_parameter2 = self.parse_input_parameters(2, parameters, memory)
        result = input_parameter1 * input_parameter2
        memory[self.parse_output_parameter(2, parameters[2], memory)] = result
        log.log(log.DEBUG, f'  {self.program_name}: Multiplication on {parameters[0]} ({input_parameter1}) and {parameters[1]} ({input_parameter2}) stored in {parameters[2]} ({result})')


class Input(Operation):
    def num_parameters(self) -> int:
        return 1
    
    def apply(self, memory: Memory, *parameters: int) -> None:
        if len(parameters) != self.num_parameters():
            raise ValueError(f'{self.program_name}: Expected {self.num_parameters()} parameters, got {parameters}')
        if self.input.empty():
            log.log(log.DEBUG, f'  {self.program_name}: Waiting on input')
        input_value = self.input.get()
        memory[self.parse_output_parameter(0, parameters[0], memory)] = input_value
        log.log(log.DEBUG, f'  {self.program_name}: Input value {input_value} written to location {parameters[0]}')


class Output(Operation):
    def num_parameters(self) -> int:
        return 1
    
    def apply(self, memory: Memory, *parameters: int) -> None:
        input_parameter, = self.parse_input_parameters(1, parameters, memory)
        self.output.put(input_parameter)
        log.log(log.DEBUG, f'  {self.program_name}: Output value {input_parameter} read from {parameters[0]}')


class LessThan(Operation):
    def num_parameters(self) -> int:
        return 3
    
    def apply(self, memory: Memory, *parameters: int) -> None:
        input_parameter1, input_parameter2 = self.parse_input_parameters(2, parameters, memory)
        result = 1 if input_parameter1 < input_parameter2 else 0
        memory[self.parse_output_parameter(2, parameters[2], memory)] = result
        log.log(log.DEBUG, f'  {self.program_name}: LessThan on {parameters[0]} ({input_parameter1}) and {parameters[1]} ({input_parameter2}) stored in {parameters[2]} ({result})')


class Equals(Operation):
    def num_parameters(self) -> int:
        return 3
    
    def apply(self, memory: Memory, *parameters: int) -> None:
        input_parameter1, input_parameter2 = self.parse_input_parameters(2, parameters, memory)
        result = 1 if input_parameter1 == input_parameter2 else 0
        memory[self.parse_output_parameter(2, parameters[2], memory)] = result
        log.log(log.DEBUG, f'  {self.program_name}: Equals on {parameters[0]} ({input_parameter1}) and {parameters[1]} ({input_parameter2}) stored in {parameters[2]} ({result})')


class JumpIfTrue(Operation):
    def num_parameters(self) -> int:
        return 2
    
    def apply(self, memory: Memory, *parameters: int) -> int | None:
        input_parameter1, input_parameter2 = self.parse_input_parameters(2, parameters, memory)
        if input_parameter1 != 0:
            log.log(log.DEBUG, f'  {self.program_name}: JumpIfTrue on {parameters[0]} ({input_parameter1}) is jumping to {parameters[1]} ({input_parameter2})')
            return input_parameter2
        log.log(log.DEBUG, f'  {self.program_name}: JumpIfTrue on {parameters[0]} ({input_parameter1}) does nothing')
        return None


class JumpIfFalse(Operation):
    def num_parameters(self) -> int:
        return 2
    
    def apply(self, memory: Memory, *parameters: int) -> int | None:
        input_parameter1, input_parameter2 = self.parse_input_parameters(2, parameters, memory)
        if input_parameter1 == 0:
            log.log(log.DEBUG, f'  {self.program_name}: JumpIfFalse on {parameters[0]} ({input_parameter1}) is jumping to {parameters[1]} ({input_parameter2})')
            return input_parameter2
        log.log(log.DEBUG, f'  {self.program_name}: JumpIfFalse on {parameters[0]} ({input_parameter1}) does nothing')
        return None


class RelativeBaseOffset(Operation):
    def num_parameters(self) -> int:
        return 1
    
    def apply(self, memory: Memory, *parameters: int) -> None:
        input_parameter, = self.parse_input_parameters(1, parameters, memory)
        memory.relative_base = input_parameter
        log.log(log.DEBUG, f'  {self.program_name}: Relative base offset by {input_parameter} (read from {parameters[0]}) to {memory.relative_base}')


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
        log.log(log.DEBUG, f'{self.name}: is starting')
        instruction_pointer = 0
        while True:
            instruction = self.memory[instruction_pointer]
            opcode, parameter_modes = self.parse_instruction(instruction)
            if opcode == 99:
                break
            operation = self.OPERATIONS[opcode](self.name, parameter_modes, self.input, self.output)
            parameters = self.memory[(instruction_pointer+1):(instruction_pointer+1+operation.num_parameters())]
            next_instruction_pointer = operation.apply(self.memory, *parameters)
            if next_instruction_pointer is not None:
                instruction_pointer = next_instruction_pointer
            else:
                instruction_pointer += 1 + operation.num_parameters()
        log.log(log.DEBUG, f'{self.name}: is done')
