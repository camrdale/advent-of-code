from abc import ABC, abstractmethod

from aoc import log


class Operation(ABC):
    def __init__(self, parameter_modes: list[int]):
        if len(parameter_modes) > self.num_parameters():
            raise ValueError(f'Operation {self} expected no more than {self.num_parameters()} parameter modes, got {parameter_modes}')
        self.parameter_modes = parameter_modes

    def parse_input_parameters(self, num_input_parameters: int, parameters: tuple[int, ...], memory: list[int]) -> list[int]:
        if len(parameters) != self.num_parameters():
            raise ValueError(f'Expected {self.num_parameters()} parameters, got {parameters}')
        parsed_parameters: list[int] = []
        for i in range(num_input_parameters):
            if i >= len(self.parameter_modes) or self.parameter_modes[i] == 0:
                parsed_parameters.append(memory[parameters[i]])
            elif self.parameter_modes[i] == 1:
                parsed_parameters.append(parameters[i])
            else:
                raise ValueError(f'Unexpected parameter mode: {self.parameter_modes[i]}')
        return parsed_parameters

    @abstractmethod
    def num_parameters(self) -> int:
        pass

    @abstractmethod
    def apply(self, memory: list[int], input: list[int], output: list[int], *parameters: int) -> None | int:
        pass


class Addition(Operation):
    def num_parameters(self) -> int:
        return 3
    
    def apply(self, memory: list[int], input: list[int], output: list[int], *parameters: int) -> None:
        input_parameter1, input_parameter2 = self.parse_input_parameters(2, parameters, memory)
        result = input_parameter1 + input_parameter2
        memory[parameters[2]] = result
        log.log(log.DEBUG, f'Addition on {parameters[0]} ({input_parameter1}) and {parameters[1]} ({input_parameter2}) stored in {parameters[2]} ({result})')


class Multiplication(Operation):
    def num_parameters(self) -> int:
        return 3
    
    def apply(self, memory: list[int], input: list[int], output: list[int], *parameters: int) -> None:
        input_parameter1, input_parameter2 = self.parse_input_parameters(2, parameters, memory)
        result = input_parameter1 * input_parameter2
        memory[parameters[2]] = result
        log.log(log.DEBUG, f'Multiplication on {parameters[0]} ({input_parameter1}) and {parameters[1]} ({input_parameter2}) stored in {parameters[2]} ({result})')


class Input(Operation):
    def num_parameters(self) -> int:
        return 1
    
    def apply(self, memory: list[int], input: list[int], output: list[int], *parameters: int) -> None:
        if not input:
            raise ValueError(f'Input operation had no input to read from')
        if len(parameters) != self.num_parameters():
            raise ValueError(f'Expected {self.num_parameters()} parameters, got {parameters}')
        input_value = input.pop(0)
        memory[parameters[0]] = input_value
        log.log(log.DEBUG, f'Input value {input_value} written to location {parameters[0]}')


class Output(Operation):
    def num_parameters(self) -> int:
        return 1
    
    def apply(self, memory: list[int], input: list[int], output: list[int], *parameters: int) -> None:
        input_parameter, = self.parse_input_parameters(1, parameters, memory)
        output.append(input_parameter)
        log.log(log.DEBUG, f'Output value {input_parameter} read from {parameters[0]}')


class LessThan(Operation):
    def num_parameters(self) -> int:
        return 3
    
    def apply(self, memory: list[int], input: list[int], output: list[int], *parameters: int) -> None:
        input_parameter1, input_parameter2 = self.parse_input_parameters(2, parameters, memory)
        result = 1 if input_parameter1 < input_parameter2 else 0
        memory[parameters[2]] = result
        log.log(log.DEBUG, f'LessThan on {parameters[0]} ({input_parameter1}) and {parameters[1]} ({input_parameter2}) stored in {parameters[2]} ({result})')


class Equals(Operation):
    def num_parameters(self) -> int:
        return 3
    
    def apply(self, memory: list[int], input: list[int], output: list[int], *parameters: int) -> None:
        input_parameter1, input_parameter2 = self.parse_input_parameters(2, parameters, memory)
        result = 1 if input_parameter1 == input_parameter2 else 0
        memory[parameters[2]] = result
        log.log(log.DEBUG, f'Equals on {parameters[0]} ({input_parameter1}) and {parameters[1]} ({input_parameter2}) stored in {parameters[2]} ({result})')


class JumpIfTrue(Operation):
    def num_parameters(self) -> int:
        return 2
    
    def apply(self, memory: list[int], input: list[int], output: list[int], *parameters: int) -> int | None:
        input_parameter1, input_parameter2 = self.parse_input_parameters(2, parameters, memory)
        if input_parameter1 != 0:
            log.log(log.DEBUG, f'JumpIfTrue on {parameters[0]} ({input_parameter1}) is jumping to {parameters[1]} ({input_parameter2})')
            return input_parameter2
        log.log(log.DEBUG, f'JumpIfTrue on {parameters[0]} ({input_parameter1}) does nothing')
        return None


class JumpIfFalse(Operation):
    def num_parameters(self) -> int:
        return 2
    
    def apply(self, memory: list[int], input: list[int], output: list[int], *parameters: int) -> int | None:
        input_parameter1, input_parameter2 = self.parse_input_parameters(2, parameters, memory)
        if input_parameter1 == 0:
            log.log(log.DEBUG, f'JumpIfFalse on {parameters[0]} ({input_parameter1}) is jumping to {parameters[1]} ({input_parameter2})')
            return input_parameter2
        log.log(log.DEBUG, f'JumpIfFalse on {parameters[0]} ({input_parameter1}) does nothing')
        return None


class Program:
    OPERATIONS: dict[int, type[Operation]] = {
        1: Addition,
        2: Multiplication,
        3: Input,
        4: Output,
        5: JumpIfTrue,
        6: JumpIfFalse,
        7: LessThan,
        8: Equals,
    }

    def __init__(self, memory: list[int]):
        self.memory = memory

    def parse_instruction(self, instruction: int) -> tuple[int, list[int]]:
        opcode = instruction % 100
        parameter_modes: list[int] = []
        remaining_instruction = instruction // 100
        while remaining_instruction > 0:
            parameter_modes.append(remaining_instruction % 10)
            remaining_instruction = remaining_instruction // 10
        return opcode, parameter_modes
    
    def run(self, input: list[int]) -> list[int]:
        output: list[int] = []
        instruction_pointer = 0
        while True:
            instruction = self.memory[instruction_pointer]
            opcode, parameter_modes = self.parse_instruction(instruction)
            if opcode == 99:
                return output
            operation = self.OPERATIONS[opcode](parameter_modes)
            parameters = self.memory[(instruction_pointer+1):(instruction_pointer+1+operation.num_parameters())]
            next_instruction_pointer = operation.apply(self.memory, input, output, *parameters)
            if next_instruction_pointer is not None:
                instruction_pointer = next_instruction_pointer
            else:
                instruction_pointer += 1 + operation.num_parameters()
