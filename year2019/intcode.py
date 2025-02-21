from abc import ABC, abstractmethod
import enum
import json
import pathlib
import queue
import threading
from typing import overload, Any, NamedTuple, Self

from aoc import log


class Memory:
    def __init__(self, initial_memory: list[int], relative_base: int = 0):
        self.memory = list(initial_memory)
        self._relative_base: int = relative_base

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
        log.log(log.INTCODE, f'Memory padded to new length: {new_len}')

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

    def __init__(self, program_name: str, parameter_modes: list[int], input: queue.Queue[int], output: queue.Queue[int], memory: Memory, blocked: threading.Event, running: threading.Event):
        if len(parameter_modes) > len(self.parameter_types):
            raise ValueError(f'{program_name}: Operation {self} expected no more than {len(self.parameter_types)} parameter modes, got {parameter_modes}')
        self.program_name = program_name
        self.parameter_modes = parameter_modes
        self.input = input
        self.output = output
        self.memory = memory
        self.blocked = blocked
        self.running = running
        self.raw_parameters: list[str] = []
        self.parsed_parameters: list[str] = []
        self.result: str = ''
        # List of memory values read from, if input parameters are immediate,
        # will contain the negative of the parameter number (starting from -1).
        self.reads_from: list[int] = []
        # Memory value written to, and value written, if any.
        self.value_written: int | None = None
        self.writes_to: int = -1

    def get_parameters(self, parameters: tuple[int, ...]) -> list[int]:
        if len(parameters) != len(self.parameter_types):
            raise ValueError(f'{self.program_name}: Expected {self.parameter_types} parameters, got {parameters}')
        parsed_parameters: list[int] = []
        for i, parameter_type in enumerate(self.parameter_types):
            self.raw_parameters.append(f'{parameters[i]}')
            if i >= len(self.parameter_modes) or self.parameter_modes[i] == 0:
                # Position mode
                self.raw_parameters[-1] += 'p'
                if parameter_type == ParameterType.INPUT:
                    parsed_parameters.append(self.memory[parameters[i]])
                    self.reads_from.append(parameters[i])
                else:
                    parsed_parameters.append(parameters[i])
            elif self.parameter_modes[i] == 1:
                # Immediate mode
                self.raw_parameters[-1] += 'i'
                if parameter_type == ParameterType.INPUT:
                    parsed_parameters.append(parameters[i])
                    self.reads_from.append(-1 - i)
                else:
                    raise ValueError(f'{self.program_name}: Unexpected immediate parameter mode for output')
            elif self.parameter_modes[i] == 2:
                # Relative mode
                self.raw_parameters[-1] += 'r'
                if parameter_type == ParameterType.INPUT:
                    parsed_parameters.append(self.memory[self.memory.relative_base + parameters[i]])
                    self.reads_from.append(self.memory.relative_base + parameters[i])
                else:
                    parsed_parameters.append(self.memory.relative_base + parameters[i])
            else:
                raise ValueError(f'{self.program_name}: Unexpected parameter mode: {self.parameter_modes[i]}')
        self.parsed_parameters = list(map(str, parsed_parameters))
        return parsed_parameters
    
    def write(self, output_location: int, value: int) -> None:
        self.memory[output_location] = value
        self.result = f'Memory[{output_location}] = {value}'
        self.writes_to = output_location
        self.value_written = value

    @abstractmethod
    def apply(self, *parameters: int) -> None | int:
        pass

    def __str__(self) -> str:
        s = [f'{self.short_name}({",".join(self.raw_parameters)})']
        s.append(f'{self.short_name}({",".join(self.parsed_parameters)})')
        s.append(self.result)
        return ' -> '.join(s)


class Addition(Operation):
    parameter_types = (ParameterType.INPUT, ParameterType.INPUT, ParameterType.OUTPUT)
    short_name = 'ADD'

    def apply(self, *parameters: int) -> None:
        input_parameter1, input_parameter2, output_location = self.get_parameters(parameters)
        result = input_parameter1 + input_parameter2
        self.write(output_location, result)


class Multiplication(Operation):
    parameter_types = (ParameterType.INPUT, ParameterType.INPUT, ParameterType.OUTPUT)
    short_name = 'MUL'
    
    def apply(self, *parameters: int) -> None:
        input_parameter1, input_parameter2, output_location = self.get_parameters(parameters)
        result = input_parameter1 * input_parameter2
        self.write(output_location, result)


class Input(Operation):
    parameter_types = (ParameterType.OUTPUT,)
    short_name = 'IN'
    
    def apply(self, *parameters: int) -> None:
        output_location, = self.get_parameters(parameters)
        if self.input.empty():
            log.log(log.DEBUG, f'  {self.program_name}: Waiting on input')
            self.running.clear()
            self.blocked.set()
        input_value = self.input.get()
        self.blocked.clear()
        self.running.set()
        self.write(output_location, input_value)


class Output(Operation):
    parameter_types = (ParameterType.INPUT,)
    short_name = 'OUT'
    
    def apply(self, *parameters: int) -> None:
        input_parameter, = self.get_parameters(parameters)
        self.output.put(input_parameter)
        self.result = f'Output {input_parameter}'


class LessThan(Operation):
    parameter_types = (ParameterType.INPUT, ParameterType.INPUT, ParameterType.OUTPUT)
    short_name = 'LT'

    def apply(self, *parameters: int) -> None:
        input_parameter1, input_parameter2, output_location = self.get_parameters(parameters)
        result = 1 if input_parameter1 < input_parameter2 else 0
        self.write(output_location, result)


class Equals(Operation):
    parameter_types = (ParameterType.INPUT, ParameterType.INPUT, ParameterType.OUTPUT)
    short_name = 'EQ'

    def apply(self, *parameters: int) -> None:
        input_parameter1, input_parameter2, output_location = self.get_parameters(parameters)
        result = 1 if input_parameter1 == input_parameter2 else 0
        self.write(output_location, result)


class JumpIfTrue(Operation):
    parameter_types = (ParameterType.INPUT, ParameterType.INPUT)
    short_name = 'JIT'

    def apply(self, *parameters: int) -> int | None:
        input_parameter1, input_parameter2 = self.get_parameters(parameters)
        if input_parameter1 != 0:
            self.result = f'JUMP {input_parameter2}'
            return input_parameter2
        self.result = 'NOOP'
        return None


class JumpIfFalse(Operation):
    parameter_types = (ParameterType.INPUT, ParameterType.INPUT)
    short_name = 'JIF'
    
    def apply(self, *parameters: int) -> int | None:
        input_parameter1, input_parameter2 = self.get_parameters(parameters)
        if input_parameter1 == 0:
            self.result = f'JUMP {input_parameter2}'
            return input_parameter2
        self.result = 'NOOP'
        return None


class RelativeBaseOffset(Operation):
    parameter_types = (ParameterType.INPUT,)
    short_name = 'RBO'
    
    def apply(self, *parameters: int) -> None:
        input_parameter, = self.get_parameters(parameters)
        self.memory.relative_base = input_parameter
        self.result = f'RelativeBase = {self.memory.relative_base}'


class ProgramState(NamedTuple):
    memory: list[int]
    relative_base: int
    instruction_pointer: int

    @classmethod
    def initial_state(cls, initial_memory: list[int]) -> Self:
        return cls(initial_memory, 0, 0)


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

    def __init__(self, name: str, memory: list[int], instruction_pointer: int = 0, relative_base: int = 0, visualize: bool = False):
        super().__init__(name=name, daemon=True)
        self.memory = Memory(memory, relative_base=relative_base)
        self.instruction_pointer = instruction_pointer
        self.visualize = visualize
        self.output_json: dict[Any, Any] = {}

    def current_state(self) -> ProgramState:
        if not self.blocked.is_set():
            log.log(log.DEBUG, f'  {self.name}: Waiting to dump state until blocked')
        self.blocked.wait()
        return ProgramState(list(self.memory.memory), self.memory.relative_base, self.instruction_pointer)
    
    @classmethod
    def from_state(cls, name: str, state: ProgramState, visualize: bool = False) -> Self:
        return cls(name, state.memory, relative_base=state.relative_base, instruction_pointer=state.instruction_pointer, visualize=visualize)

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
        if self.visualize:
            self.output_json['initial_state'] = {
                'memory': list(self.memory.memory),
                'input': list(input.queue),
                'output': list(output.queue),
                'relative_base': self.memory.relative_base,
            }
            self.output_json['operations'] = []
        self.blocked = threading.Event()
        self.running = threading.Event()
        self.done = False
        self.start()

    def run(self) -> None:
        log.log(log.DEBUG, f'{self.name}: is starting')
        self.running.set()
        num_instructions = 0
        while True:
            instruction = self.memory[self.instruction_pointer]
            num_instructions += 1
            opcode, parameter_modes = self.parse_instruction(instruction)
            if opcode == 99:
                break
            operation = self.OPERATIONS[opcode](self.name, parameter_modes, self.input, self.output, self.memory, self.blocked, self.running)
            num_params = len(operation.parameter_types)
            parameters = self.memory[(self.instruction_pointer+1):(self.instruction_pointer+1+num_params)]
            next_instruction_pointer = operation.apply(*parameters)
            log.log(log.INTCODE, f'  {self.name} {instruction:5d}: {operation}')
            if self.visualize:
                input_parameter_locations = operation.reads_from
                for i, input_parameter_location in enumerate(input_parameter_locations):
                    if input_parameter_location < 0:
                        input_parameter_locations[i] = self.instruction_pointer + abs(input_parameter_location)
                operation_json = {
                    'instruction_pointer': self.instruction_pointer,
                    'instruction': instruction,
                    'num_parameters': num_params,
                    'short_name': operation.short_name,
                    'operation_description': str(operation),
                    'input': list(self.input.queue),
                    'output': list(self.output.queue),
                    'relative_base': self.memory.relative_base,
                    'input_parameter_locations': input_parameter_locations,
                }
                if operation.value_written is not None:
                    operation_json['output_location'] = operation.writes_to
                    operation_json['output_value'] = operation.value_written
                self.output_json['operations'].append(operation_json)
            if next_instruction_pointer is not None:
                self.instruction_pointer = next_instruction_pointer
            else:
                self.instruction_pointer += 1 + num_params
        log.log(log.DEBUG, f'{self.name}: is done, ran {num_instructions} instructions')
        if self.visualize:
            with (pathlib.Path(__file__).parent.resolve() / 'visualizer' / 'dumps' / f'{self.name}.json').open('w') as f:
                json.dump(self.output_json, f, separators=(',', ':'))
        self.done = True
        self.blocked.set()


class SynchronousProgram:
    def __init__(self, name: str, memory: list[int], instruction_pointer: int = 0, relative_base: int = 0, visualize: bool = False):
        self.program = Program(name, memory, instruction_pointer=instruction_pointer, relative_base=relative_base, visualize=visualize)
        self.output: list[int] = []
        self.start_of_latest_output = 0
        self.program_input: queue.Queue[int] = queue.Queue()
        self.program_output: queue.Queue[int] = queue.Queue()
        self.program.execute(self.program_input, self.program_output)
        self._read_output()

    def _read_output(self) -> None:
        self.program.blocked.wait()
        while not self.program_output.empty():
            self.output.append(self.program_output.get_nowait())

    def write(self, input: list[int]) -> None:
        if self.program.done:
            raise ValueError(f'Program already terminated, cant write: {input}')
        self.start_of_latest_output = len(self.output)
        running_waiter = threading.Thread(target=self.program.running.wait, daemon=True)
        running_waiter.start()
        for i in input:
            self.program_input.put(i)
        running_waiter.join()
        self._read_output()

    def write_ascii(self, ascii_input: str) -> None:
        if self.program.done:
            raise ValueError(f'Program already terminated, cant write: {ascii_input}')
        if ascii_input[-1] != '\n':
            ascii_input += '\n'
        log.log(log.INFO, ascii_input)
        self.write([ord(c) for c in ascii_input])

    def is_done(self) -> bool:
        return self.program.done
    
    def get_latest_output(self) -> list[int]:
        return self.output[self.start_of_latest_output:]
    
    def get_latest_output_ascii(self) -> str:
        ascii_output = ''
        for output in self.get_latest_output():
            if output > 127:
                log.log(log.DEBUG, f'Ignoring non-ascii character: {output}')
                continue
            ascii_output += chr(output)
        return ascii_output
