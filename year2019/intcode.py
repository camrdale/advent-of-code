from abc import ABC, abstractmethod

from aoc import log


class Operation(ABC):
    @abstractmethod
    def parameters(self) -> int:
        pass

    @abstractmethod
    def apply(self, memory: list[int], *parameters: int) -> None:
        pass


class Addition(Operation):
    def parameters(self) -> int:
        return 3
    
    def apply(self, memory: list[int], *parameters: int) -> None:
        if len(parameters) != self.parameters():
            raise ValueError(f'Expected {self.parameters()} parameters, got {parameters}')
        input1, input2, output = parameters
        result = memory[input1] + memory[input2]
        memory[output] = result
        log.log(log.DEBUG, f'Addition on {input1} ({memory[input1]}) and {input2} ({memory[input2]}) stored in {output} ({result})')


class Multiplication(Operation):
    def parameters(self) -> int:
        return 3
    
    def apply(self, memory: list[int], *parameters: int) -> None:
        if len(parameters) != self.parameters():
            raise ValueError(f'Expected {self.parameters()} parameters, got {parameters}')
        input1, input2, output = parameters
        result = memory[input1] * memory[input2]
        memory[output] = result
        log.log(log.DEBUG, f'Multiplication on {input1} ({memory[input1]}) and {input2} ({memory[input2]}) stored in {output} ({result})')


class Program:
    OPERATIONS: dict[int, Operation] = {
        1: Addition(),
        2: Multiplication(),
    }

    def __init__(self, memory: list[int]):
        self.memory = memory
    
    def run(self):
        instruction_pointer = 0
        while True:
            opcode = self.memory[instruction_pointer]
            if opcode == 99:
                return
            operation = self.OPERATIONS[opcode]
            parameters = self.memory[(instruction_pointer+1):(instruction_pointer+1+operation.parameters())]
            operation.apply(self.memory, *parameters)
            instruction_pointer += 1 + operation.parameters()
