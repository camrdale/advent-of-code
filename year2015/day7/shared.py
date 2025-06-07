import re


INSTRUCTION = re.compile(r'([0-9a-z]* )?(AND |LSHIFT |NOT |OR |RSHIFT )?([0-9a-z]*) -> ([a-z]*)')
MASK_16_BITS = 0xFFFF


class Operation:
    def __init__(self) -> None:
        self.initialized = False
        self.lhs: int | Operation
        self.rhs: int | Operation
        self.operation: str | None = None
        self._value: int | None = None
    
    @classmethod
    def parse_text(cls, text: str) -> re.Match[str]:
        instruction = INSTRUCTION.match(text)
        if instruction is None:
            raise ValueError(f'Failed to parse: {text}')
        return instruction
    
    def parse_operand(self, operand: str, operations: dict[str, 'Operation']) -> 'int | Operation':
        if operand[0].isdigit():
            return int(operand)
        return operations[operand]

    def initialize(self, instruction: re.Match[str], operations: dict[str, 'Operation']) -> None:
        self.initialized = True
        if instruction.group(1) is not None:
            self.lhs = self.parse_operand(instruction.group(1).strip(), operations)
        if instruction.group(2) is not None:
            self.operation = instruction.group(2).strip()
        self.rhs = self.parse_operand(instruction.group(3), operations)
        self.name = instruction.group(4)

    def get_value(self, operand: 'int | Operation') -> int:
        return operand if isinstance(operand, int) else operand.value()

    def value(self) -> int:
        if self._value is not None:
            return self._value
        if not self.initialized:
            raise ValueError(f'Operation not yet initialized')
        match self.operation:
            case None:
                self._value = self.get_value(self.rhs)
            case 'NOT':
                self._value = (~self.get_value(self.rhs)) & MASK_16_BITS
            case 'LSHIFT':
                self._value = (self.get_value(self.lhs) << self.get_value(self.rhs)) & MASK_16_BITS
            case 'AND':
                self._value = self.get_value(self.lhs) & self.get_value(self.rhs)
            case 'OR':
                self._value = self.get_value(self.lhs) | self.get_value(self.rhs)
            case 'RSHIFT':
                self._value = self.get_value(self.lhs) >> self.get_value(self.rhs)
            case _:
                raise ValueError(f'Operation {self.name} has unexpected operation {self.operation}')
        return self._value

    def reset(self):
        self._value = None

    def set_value(self, value: int):
        self._value = value
